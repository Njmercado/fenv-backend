from models.user_model import UserModel
from utils.crypto_utils import Cipher
from environs import Env
import base64

env = Env()
env.read_env()
key_phrase = bytes(env("CIPHER_KEYPHRASE"), "utf-8")

cipher = Cipher()
cipher.key_phrase = base64.b64decode(key_phrase)

def __cipherData(data):
  formated_data = cipher.addBufferToData(data)
  nonce = cipher.generateNonce()
  crypted_data = cipher.encrypt(formated_data, nonce)   
  final_data = cipher.appendNonceToData(crypted_data, nonce)
  return final_data


def __decipherData(data):
  data = bytes(data, encoding="utf-8")
  decoded_data = base64.b64decode(data)
  data, nonce = cipher.splitCipherData(decoded_data)
  decrypted_data = cipher.decrypt(data, nonce)
  data_without_buffer = cipher.dataWithoutBuffer(decrypted_data)
  return data_without_buffer

def __userExists(user_email):
  response = UserModel.objects(email=user_email)
  return True if bool(len(response)) else False

def create_user(params):

  print(params.email)

  if not __userExists(params.email):
    ciphered_password = __cipherData(params.password)
    user_model = UserModel(
      name=params.name,
      password=ciphered_password,
      email=params.email,
    )
    user_model.save()
  else:
    return {
      "message": "This user already exist, plis try to recover your password",
      "error": False
    }
  return {
    "message": "User created successfully",
    "error": False
  } 