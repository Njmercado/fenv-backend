import re
from random import randint

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters_len = len(letters)
numbers = "1234567890"
numbers_len = len(numbers)
special_characters = "°!#$%&/()=\"\'?¿¡\\*+]}{[~,.;:<>-_@"
special_characters_len = len(special_characters)

def randomLetters(length):
  random_letters = ""
  for i in range(length):
    random_number = randint(1, letters_len) - 1
    random_letters += letters[random_number]
  return random_letters

def randomNumbers(length):
  random_numbers = ""
  for i in range(length):
    random_number = randint(1, numbers_len) - 1
    random_numbers += numbers[random_number]
  return random_numbers

def randomSpecialCharacters(length):
  random_special_characters = ""
  for i in range(length):
    random_number = randint(1, special_characters_len) - 1
    random_special_characters += special_characters[random_number]
  return random_special_characters

def generatePassword(length):
  password = ""

  for i in range(length):
    random_number = randint(0, 2)
    if random_number == 0: password += randomLetters(1)
    if random_number == 1: password += randomNumbers(1)
    if random_number == 2: password += randomSpecialCharacters(1)

  return password

def verifyPassword(password):

  is_valid = True

  has_uppercases = re.search(r"[A-Z]", password)
  has_lowercases = re.search(r"[a-z]", password)
  has_numbers = re.search(r"\d", password)
  has_special_characters = re.search(r"\°|\!|\#|\$|\%|\&|/|\(|\)|\=|\"|\'|\?|\¿|\¡|\*|\+|\{|\[|\]|\}|\~|\,|\.|\;|\:|\<|\>|\-|\_|\@", password)

  if not has_uppercases: is_valid = False
  if not has_lowercases: is_valid = False
  if not has_numbers: is_valid = False
  if not has_special_characters: is_valid = False
  if not len(password) >= 10: is_valid = False

  return is_valid
