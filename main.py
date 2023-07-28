import os
from os.path import join, dirname
from dotenv import load_dotenv

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from firebase_admin import auth, credentials
import firebase_admin

from utils.write_memories import WriterGPT
from utils.authenticate import get_current_user

# for environment_val
dotenv_path = join(dirname(__file__), "./ENV/.env")
load_dotenv(dotenv_path)

# for authentication
footprint_with_FBA="./ENV/footprint_FBA.json"
cred = credentials.Certificate(footprint_with_FBA)
firebase_admin.initialize_app(cred)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   
    allow_methods=["*"],      
    allow_headers=["*"]       
)

class HealthModel(BaseModel):
    message: str

@app.get("/health", response_model=HealthModel)
async def health():
    return HealthModel(message=f"Welcome to footprint &#x1f43e;")

@app.get("/who_is_me")
async def who_is_me(current_user=Depends(get_current_user)):
    return {"msg": "Hello", "uid": current_user}
