from fastapi import APIRouter , Depends  , HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserModel , UserRegister
from ..dependencies import get_db
from services.user_service import create_user , verify_user_is_exists
from services.auth_service import verify_token , create_token


auth_router = APIRouter(prefix='/auth' ,tags=["authentication"])


@auth_router.get('/')
def hello():
    return 'hello'


@auth_router.post('/register')
def register(user:UserRegister , db:Session=Depends(get_db)):
    user_exists = verify_user_is_exists(user , db)
    print(user_exists)
    if user_exists:
        raise HTTPException(
        detail="Email deja exists"
    )
    else:
        return create_user(user , db)



@auth_router.post('/login')
def login(user:UserModel , db:Session = Depends(get_db)):
    user_exists = verify_user_is_exists(user , db)
    if user_exists:
        user_dict = user.model_dump()
        token = create_token(user_dict)
        return {
            'success':'you logged successfully',
            'token': token
            }
    raise HTTPException(
        status_code=401,
        detail="Email ou mot de passe incorrect"
    )


@auth_router.post("/logout")
def logout():
    return {"message": "OK"}
