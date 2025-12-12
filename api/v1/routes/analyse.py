from fastapi import APIRouter , Depends , HTTPException
from services.analyze_services import create_prompt , analyse_with_gemini , create_new_analysis_log
from ..schemas.analysis_logs import AnalysisLog
from services.auth_service import verify_token
from sqlalchemy.orm import Session
from api.v1.dependencies import get_db
from db.models.user import User
from utils.hashing import verify_password


analyse_router = APIRouter(prefix='/analysis', tags=['analysis'])


@analyse_router.post('/analyse')
def analyse_text(text : str , current_user = Depends(verify_token) , db: Session = Depends(get_db)):
     
     prompt , score , label = create_prompt(text)
     resume_context =  analyse_with_gemini(prompt)
     
     
     result = {
          "text":text,
          "score":score,
          "category":label,
          "ton":resume_context['ton'],
          "resume":resume_context['resume']
     }
     
     print(result)
     user = db.query(User).filter(User.email == current_user['email']).first()
     print('--------------------------- ' , current_user)
     if not user:
         raise HTTPException(status_code=404, detail="User not found")
    
     print(current_user['password'], user.password_hash)
     
     if not verify_password(current_user['password'], user.password_hash):
          raise HTTPException(status_code=401, detail="Invalid credentials")

     print(user)
     new_log = create_new_analysis_log(result , user , db)
     
     return new_log
    