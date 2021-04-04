from models.user_model import UserModel
from utils.crypto_utils import Cipher
from utils.password import verifyPassword
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

def verifyUser(user):
  response = UserModel.objects(email=user["email"]).first()

  if not response: return False

  deciphered_password = __decipherData(response["password"])
  return user["password"] == deciphered_password

def getUser(user_email):
  user = UserModel.objects(email = user_email).first()
  return user

def userExists(user_email):
  response = UserModel.objects(email=user_email)
  return True if bool(len(response)) else False

def createUser(params):
  
  is_valid_password = not verifyPassword(params.password)

  if is_valid_password: return { "message": "Wrong password, please enter a valid one", "error": True, "data": None }

  if not userExists(params.email):
    ciphered_password = __cipherData(params.password)
    user_model = UserModel(
      name=params.name,
      password=ciphered_password,
      email=params.email,
    )
    user_model.save()
  else:
    return {
      "message": "This user already exist, plis try to recover your password if you dont remember it",
      "error": True
    }
  return { "message": "User created successfully", "error": False, "data": None } 

def changePassword(user_email: str, new_password: str):
  try:
    user = getUser(user_email)

    is_valid_password = verifyPassword(new_password)
    if not is_valid_password: return { "message": "Wrong password, please enter a valid one", "error": True, "data": None} 

    ciphered_new_password = __cipherData(new_password)
    user.password = ciphered_new_password
    user.save()
    return {"message": "password changed correctly", "error": False, "data": None}
  except Exception as error:
    print(f"Some has happend changing user password in user_consumer.py. error: {error}")
    return {"message": f"Some error has happend: {error}", "error": True, "data": None}
