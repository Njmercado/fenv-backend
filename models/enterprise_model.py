from environs import Env
from mongoengine import connect, EmbeddedDocument, UUIDField, StringField, EmailField, DateTimeField, EmbeddedDocumentListField
from models.project_model import ProjectModel
import datetime, uuid

env = Env()
env.read_env()

connect(
  db=env("MONGODB_DATABASE"),
  username=env("MONGODB_USERNAME"),
  password=env("MONGODB_PASSWORD"),
  authentication_source="p64b",
  host=env("MONGODB_DATABASE"),
  port=27017
)

class EnterpriseModel(EmbeddedDocument):
  id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
  name = StringField(editable=True, max_length=100, required=True)
  projects = EmbeddedDocumentListField(ProjectModel)
  created_at = DateTimeField(default=datetime.datetime.now())
