from core.models import action
from core import helpers, logging, auth
import smtplib, re

class _email(action._action):
	to = str()
	sender = str()
	password = str()
	host = str()
	port = 25
	subject = str()
	body = str()
	html = bool()

	def run(self,data,persistentData,actionResult):
		from email.mime.text import MIMEText
		body = helpers.evalString(self.body,{"data" : data})
		subject = helpers.evalString(self.subject,{"data" : data})
		if self.password.startswith("ENC") and self.password != "":
			password = auth.getPasswordFromENC(self.password)
		elif "%%" in self.password:
			password = helpers.evalString(self.password,{"data" : data["flowData"]})
		else:
			password = ""
		if self.html:
			msg = MIMEText(body,"html")
		else:
			msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = self.sender
		msg['To'] = self.to
		print(password)
		if password != "":		
			self.sendEmailAuth(msg, smtplib.SMTP(self.host, self.port), self.sender, password)
		else:
			self.sendEmail(msg, smtplib.SMTP(self.host, self.port))
		
		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult

	def sendEmail(self, message, server):
		mailServer = server
		mailServer.send_message(message)

	def sendEmailAuth(self, message, server, sender, password):
			mailServer = server
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.login(sender, password)
			mailServer.send_message(message)
			mailServer.quit()

	def setAttribute(self,attr,value,sessionData=None):
		if attr == "password" and not value.startswith("ENC ") and not re.match(".*%%.*%%",value):
			self.password = "ENC {0}".format(auth.getENCFromPassword(value))
			return True
		return super(_email, self).setAttribute(attr,value,sessionData=sessionData)