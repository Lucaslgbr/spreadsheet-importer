from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException, Query
from pydantic import BaseModel
from app.core.services.import_service import ImportService
from app.adapters.database import Database
from app.adapters.auth_adapter import AuthAdapter
from app.core.middleware.auth_middleware import JWTBearer
from fastapi.responses import JSONResponse
import asyncio

router = APIRouter()
auth_adapter = AuthAdapter()

db_adapter = Database()
import_service = ImportService(db_adapter=db_adapter)

@router.post("/uploadfile/")
async def upload_file(
    name: str = Form(...),
    file: UploadFile = File(...), 
    user_id: str = Form(...), 
    token: str = Depends(JWTBearer(auth_adapter))
):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    try:
        asyncio.create_task(import_service.import_spreadsheet(file_path, user_id, name))        
        return JSONResponse(content={"message": "Processamento iniciado"})
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
@router.get("/get_list/")
async def get_list(
    user_id: str = Query(...),
    token: str = Depends(JWTBearer(auth_adapter))
):
    try:
        spreadsheets = db_adapter.get_spreadsheets_by_user(user_id)
        return {"data": spreadsheets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))