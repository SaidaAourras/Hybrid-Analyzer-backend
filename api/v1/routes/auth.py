from fastapi import APIRouter , Depends 
from sqlalchemy.orm import Session
from ..schemas.user import UserModel
from ..dependencies import get_db
from services.auth_service import create_user


auth_router = APIRouter(prefix='/auth' ,tags=["authentication"])


@auth_router.get('/')
def hello():
    return 'hello'

@auth_router.post('/register')
def register(user:UserModel , db:Session=Depends(get_db)):
    return create_user(user , db)
