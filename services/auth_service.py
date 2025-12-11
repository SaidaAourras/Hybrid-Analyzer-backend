from jose import jwt , JWTError
from dotenv import load_dotenv
from db.models.user import User
import os
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from fastapi import Depends , HTTPException , status
from api.v1.dependencies import get_db
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
bearer_scheme = HTTPBearer()



# create token
def create_token(payload):
    token = jwt.encode(payload , SECRET_KEY)
    return token


# verify token cridentials is the current user
def verify_token( credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme) , db = Depends(get_db)):
    token = credentials.credentials
    print(token)
    try:
        payload = jwt.decode(token , SECRET_KEY)
        return payload
    except JWTError as e:
        return e

