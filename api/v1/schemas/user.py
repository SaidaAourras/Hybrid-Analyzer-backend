from pydantic import BaseModel

class UserModel(BaseModel):
    email: str
    password: str
    
class UserRegister(UserModel):
    username: str
    
