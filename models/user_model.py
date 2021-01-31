from environs import Env
from mongoengine import connect, Document, UUIDField, StringField, ListField, StringField, EmailField, DateTimeField
import datetime, uuid

env = Env()
env.read_env()

connect(
  db=env("MONGODB_DATABASE"),
  username=env("MONGODB_ROOT_USERNAME"),
  password=env("MONGODB_ROOT_PASSWORD"),
  authentication_source="admin",
  host=env("MONGODB_DATABASE"),
  port=27017
)

class UserModel(Document):
  id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
  name = StringField(editable=True, max_length=100, required=True)
  password = StringField(editable=True, max_length=256, required=True)
  email = EmailField(required=True)
  enterprises = ListField(UUIDField(editable=False)) 
  records = ListField(UUIDField(editable=False))
  created_at = DateTimeField(default=datetime.datetime.now())

  def save(self, *args, **kwargs):
    return super(UserModel, self).save(*args, **kwargs)
