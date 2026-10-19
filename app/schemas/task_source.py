import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.task_source import InputType


class TaskSourceCreate(BaseModel):
    input_type: InputType
    raw_input: str = Field(min_length=1, max_length=20000)


class TaskSourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: uuid.UUID
    input_type: InputType
    raw_input: str
    processed_at: datetime | None
    created_at: datetime