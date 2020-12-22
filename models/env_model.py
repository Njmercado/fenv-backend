from environs import Env
from mongoengine import connect, Document, EmbeddedDocument, UUIDField, StringField, DateTimeField, EmbeddedDocumentListField
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

class AvailableIPs(EmbeddedDocument):
  ip = StringField(editable=True, max_length=12, required=True)
  available_time = DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1), require=False)

class KeyModel(EmbeddedDocument):
  id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
  name = StringField(editable=False, max_length=20, required=True)
  value = StringField(editable=True, max_length=256, required=True)
  created_at = DateTimeField(default=datetime.datetime.now())

class EnvModel(EmbeddedDocument):
  id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
  name = StringField(editable=True, max_length=100, required=True)
  available_ips = EmbeddedDocumentListField(AvailableIPs)
  key_list = EmbeddedDocumentListField(KeyModel)
  created_at = DateTimeField(default=datetime.datetime.now())
