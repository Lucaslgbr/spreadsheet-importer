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
from fastapi.responses import JSONResponse

router = APIRouter()
auth_adapter = AuthAdapter()

db_adapter = Database()
import_service = ImportService(db_adapter=db_adapter)

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), 
    user_id: str = Form(...), 
    token: str = Depends(JWTBearer(auth_adapter))
):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    try:
        import_service.import_spreadsheet(file_path, user_id)
        return JSONResponse(content={"message": "File uploaded and processed successfully."})
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
    
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
