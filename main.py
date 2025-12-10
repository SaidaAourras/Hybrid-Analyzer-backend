from fastapi import FastAPI
from db.database import engine
from db.models.base import Base
from api.v1.routes.auth import auth_router
from api.v1.routes.analyse import analyse_router
from fastapi.middleware import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

app.include_router(auth_router , prefix='/api/v1')
app.include_router(analyse_router , prefix='/api/v1')





