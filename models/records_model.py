from environs import Env
from mongoengine import connect, EmbeddedDocument, UUIDField, StringField, DateTimeField
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

class RecordModel(EmbeddedDocument):
  id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
  description = StringField(editable=False, max_length=100, required=True)
  action = StringField(choices={'DELETE', 'UPDATE', 'CREATE', 'LOGGED'}, required=True)
  ip = StringField(editable=False, required=True)
  created_at = DateTimeField(default=datetime.datetime.now())
