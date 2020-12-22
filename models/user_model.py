from environs import Env
from mongoengine import connect, Document, UUIDField, StringField, StringField, EmailField, DateTimeField, EmbeddedDocumentListField
import datetime, uuid
from models.enterprise_model import EnterpriseModel

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
  enterprises = EmbeddedDocumentListField(EnterpriseModel)
  created_at = DateTimeField(default=datetime.datetime.now())

  def save(self, *args, **kwargs):
    return super(UserModel, self).save(*args, **kwargs)