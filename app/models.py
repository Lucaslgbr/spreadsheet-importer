
from pydantic import BaseModel, Field, EmailStr


class FileSchema(BaseModel):
    name: str = Field(...)
    user_email: EmailStr = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "pagamentos_teste.csv",
                "user_email": "admin@admin.com",
            }
        }