from db.models.user import User
from utils.hashing import get_hash_password

def create_user(user , db):
    new_user = User(
        username = user.username,
        email = user.email,
        password_hash = get_hash_password(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user