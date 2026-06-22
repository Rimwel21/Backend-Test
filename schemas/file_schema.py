from pydantic import BaseModel
from datetime import datetime
from utils.enum import FileCategory

class FileOut(BaseModel):
    id: int
    filename: str
    file_type: str
    file_url: str
    file_category: FileCategory
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True