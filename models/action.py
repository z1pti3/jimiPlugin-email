from core.models import action
from core import helpers, logging
import subprocess, functools

class _email(action._action):
	to = str()
	sender = str()
	host = str()
	subject = str()
	body = str()
	html = bool()

	def run(self,data,persistentData,actionResult):
		import smtplib
		from email.mime.text import MIMEText
		body = helpers.evalString(self.body,{"data" : data})
		subject = helpers.evalString(self.subject,{"data" : data})
		if self.html:
			msg = MIMEText(body,"html")
		else:
			msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = self.sender
		msg['To'] = self.to
		self.sendEmail(msg, smtplib.SMTP(self.host))
		
		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult

	def sendEmail(self, message, server):
		mailServer = server
		mailServer.send_message(message)