from mongoengine import Document
from mongoengine import StringField, BooleanField, ReferenceField


class Users(Document):
    user_name = StringField(max_length=240, required=True, unique=True)
    user_password = StringField(max_length=240)

    def get_user_id(self):
        return self.id

    def get_user_name(self):
        self.user_name

    @staticmethod
    def get_user_object(user_name, user_password):
        return Users.objects(user_name=user_name, user_password=user_password)


class Tasks(Document):
    task_text = StringField(max_length=240, required=True)
    task_status = BooleanField()
    user_id = ReferenceField(Users)

    def get_task_id(self):
        return self.id

    def get_task_text(self):
        return self.task_text

    def get_task_status(self):
        return self.get_task_status()

    @staticmethod
    def get_task_object(user_id):
        return Tasks.objects(user_id=user_id)