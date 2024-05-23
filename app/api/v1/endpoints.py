from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from pydantic import EmailStr, BaseModel
from core.services.import_service import ImportService
from core.services.publish_service import PublishService
from adapters.csv_reader import CsvReader
from adapters.database import Database
from adapters.auth_adapter import AuthAdapter
from adapters.rabbitmq_adapter import RabbitMQAdapter
from core.middleware.auth_middleware import JWTBearer

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    user_email: EmailStr = Form(...), 
    token: str = Depends(JWTBearer(AuthAdapter()))
):
    csv_reader = CsvReader()
    db_adapter = Database()
    import_service = ImportService(csv_reader, db_adapter)
    
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    
    import_service.import_spreadsheet(file_location)
    return {"filename": file.filename}

class MessageModel(BaseModel):
    email: str
    details: str
    user: str

@router.post("/publish")
async def publish_message(message: MessageModel):
    try:
        rabbitmq_adapter = RabbitMQAdapter()
        publish_service = PublishService(rabbitmq_adapter)
        publish_service.publish_message(message.dict())
        return {"status": "Message published"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
