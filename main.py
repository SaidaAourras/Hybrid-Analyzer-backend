from fastapi import FastAPI
from db.database import engine
from db.models.base import Base
from api.v1.routes.auth import auth_router

app = FastAPI()


Base.metadata.create_all(engine)

app.include_router(auth_router , prefix='/api/v1')



