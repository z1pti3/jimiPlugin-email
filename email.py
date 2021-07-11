from core import plugin, model

class _email(plugin._plugin):
    version = 2.1

    def install(self):
        # Register models
        model.registerModel("email","_email","_action","plugins.email.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("email","_email","_action","plugins.email.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        # Auto updating subject and body for new string match %% instead of the old %
        if self.version < 1.1:
            from plugins.email.models import action
            objects = action._email().api_getByModelName("email")["results"]
            for objectItem in objects:
                loadedAction = action._email().get(objectItem["_id"])
                if "%" in loadedAction.subject:
                    loadedAction.subject = loadedAction.subject.replace("%","%%")
                    loadedAction.update(["subject"])
                if "%" in loadedAction.body:
                    loadedAction.body = loadedAction.body.replace("%","%%")
                    loadedAction.update(["body"])
