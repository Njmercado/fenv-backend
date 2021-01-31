from environs import Env
from mongoengine import connect, Document, UUIDField, StringField, EmailField, DateTimeField, ListField
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

class EnterpriseModel(Document):
  id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
  name = StringField(editable=True, max_length=100, required=True)
  projects = ListField(UUIDField(editable=False))
  created_at = DateTimeField(default=datetime.datetime.now())
