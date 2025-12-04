from jose import jwt
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

# create token
def create_token(payload):
    token = jwt.encode(payload , SECRET_KEY)
    return token


# verify token cridentials is the current user
def verify_token(token):
    my_token = token
    payload = jwt.decode(my_token , SECRET_KEY)
    return payload
