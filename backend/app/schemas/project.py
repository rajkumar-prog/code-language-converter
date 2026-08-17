from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
    source_language: str = Field(min_length=1, max_length=50)
    target_language: str = Field(min_length=1, max_length=50)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    target_language: Optional[str] = Field(default=None, min_length=1, max_length=50)


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str
    source_language: str
    target_language: str
    created_at: datetime
    updated_at: datetime
    file_count: int = 0

    model_config = {"from_attributes": True}


class FileCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    filepath: str = Field(default="", max_length=500)
    source_content: str


class FileOut(BaseModel):
    id: int
    project_id: int
    filename: str
    filepath: str
    source_content: str
    converted_content: str
    status: str
    error_message: str
    fixes_applied: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversionHistoryOut(BaseModel):
    id: int
    file_id: int
    version: int
    status: str
    errors_found: str
    fixes_applied: str
    created_at: datetime

    model_config = {"from_attributes": True}
