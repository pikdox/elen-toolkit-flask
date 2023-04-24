import hashlib, os

from MicroDB import MicroDB

from dotenv import load_dotenv
load_dotenv()

sec_db = MicroDB('sec_db','./db/')

_login_secretkey = str(os.getenv('login_secretkey'))
_security_salt = str(os.getenv('security_salt'))

# craft a default hash for password checks and other things
def craft_hash(key:str):
  return hashlib.sha512(str(key+_security_salt).encode('utf-8')).hexdigest()

# Value compare for password check like hash_compare(input_password, password_on_database)
def hash_compare(non_hashed:str,hashed:str):
  hash = craft_hash(non_hashed)
  if hash == hashed:
    return True
  return False

# craft a hash for use on auth cookies
def craft_login_hash(username:str,password:str,skip_password_hash:bool=False):
  if skip_password_hash:
    hash = craft_hash(username+password)
  else:
    password = craft_hash(password)
    hash = craft_hash(username+password)

  login_hash = craft_hash(hash+_login_secretkey)
  return login_hash

def write_log(text:str):
  pass

def clear_logs():
  pass


print(craft_hash('2222'))

