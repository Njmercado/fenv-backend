import math
import random
import os
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class Cipher:
  def __init__(self, key_phrase=""):
    self.key_phrase = key_phrase

  def addBufferToData(self, data):
    data_len = len(data)
    template_buffer = " .-.-.-.-.-.-.-.-"
    if data_len % 16 != 0:
      buffer_to_add = abs(data_len - (16*math.ceil(data_len/16)))
      formated_data = data + template_buffer[:buffer_to_add]
      return formated_data
    return data

  def appendNonceToData(self, data, nonce):
    return base64.b64encode(data+nonce)

  def generateKeyPhrase(self):
    key = get_random_bytes(16)
    return key

  def generateNonce(self):
    nonce = get_random_bytes(16)
    return nonce

  def splitCipherData(self, cipher_data):
    return cipher_data[:-16], cipher_data[-16:]

  def encrypt(self, data, nonce):
    aes = AES.new(self.key_phrase, AES.MODE_CBC, nonce)
    cipher_data = aes.encrypt(data)
    return cipher_data

  def dataWithoutBuffer(self, data):
    decrypted_data_without_buffer = data.decode("utf-8").split(" ")[:-1]
    joined_data = ' '.join(decrypted_data_without_buffer)
    return joined_data

  def decrypt(self, data, nonce):
    aes = AES.new(self.key_phrase, AES.MODE_CBC, nonce)
    decrypted_data = aes.decrypt(data)
    return decrypted_data