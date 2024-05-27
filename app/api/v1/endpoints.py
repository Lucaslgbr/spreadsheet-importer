from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from pydantic import EmailStr, BaseModel
from app.core.services.import_service import ImportService
from app.core.services.publish_service import PublishService
from app.adapters.csv_reader.csv_reader_model1 import CsvReaderModel1
from app.adapters.csv_reader.csv_reader_model2 import CsvReaderModel2
from app.adapters.csv_reader.csv_reader_model3 import CsvReaderModel3
from app.adapters.csv_reader.csv_reader_model4 import CsvReaderModel4
from app.adapters.database import Database
from app.adapters.auth_adapter import AuthAdapter
from app.adapters.rabbitmq_adapter import RabbitMQAdapter
from app.core.middleware.auth_middleware import JWTBearer

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    user_email: EmailStr = Form(...), 
    model_type: int = Form(...), 
    token: str = Depends(JWTBearer(AuthAdapter()))
):
    if model_type == 1:
        csv_reader = CsvReaderModel1()
    elif model_type == 2:
        csv_reader = CsvReaderModel2()
    elif model_type == 3:
        csv_reader = CsvReaderModel3()
    elif model_type == 4:
        csv_reader = CsvReaderModel4()
    else:
        raise HTTPException(status_code=400, detail="Invalid model type")

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
