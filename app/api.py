from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form, Query
from app.auth.auth_bearer import JWTBearer
from fastapi.middleware.cors import CORSMiddleware
from app.models import FileSchema
from pydantic import EmailStr
from app.rabbitmq import publish_to_rabbitmq

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
async def upload_file(
    file: UploadFile = File(...), 
    user_email: EmailStr = Form(...), 
    token: str = Depends(JWTBearer())
):
    # if not file.filename.endswith('.csv'):
    #     raise HTTPException(status_code=400, detail="Por favor, envie um arquivo CSV.")
    
    file_data = FileSchema(name=file.filename, user_email=user_email)
    upload_files.append(file_data)
    message = {
        "email": user_email,
        "details": "Planilha processada",
        "user": user_email
    }
    publish_to_rabbitmq(message)
    return {"data": 'Processamento de dados iniciado'}

@app.get("/get_list/")
async def get_list(
    token: str = Depends(JWTBearer()), 
    user_email: EmailStr = Query(...)
):
    filtered_files = [file for file in upload_files if file.user_email == user_email]
    return {"data": filtered_files}