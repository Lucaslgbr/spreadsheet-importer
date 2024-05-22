from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
import pandas as pd
from app.auth.auth_bearer import JWTBearer
from fastapi.middleware.cors import CORSMiddleware


upload_files = []

app = FastAPI()

origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), token: str = Depends(JWTBearer())):
    if not file.filename.endswith('.xls'):
        raise HTTPException(status_code=400, detail="Por favor, envie um arquivo XLS.")
    
    return {"data": 'Leitura de dados', "token": token}
