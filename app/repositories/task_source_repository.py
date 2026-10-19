import uuid

from sqlalchemy.orm import Session

from app.models.task_source import InputType, TaskSource


def create(db: Session, user_id: uuid.UUID, input_type: InputType, raw_input: str) -> TaskSource:
    source = TaskSource(user_id=user_id, input_type=input_type, raw_input=raw_input)
    db.add(source)
    db.commit()
    db.refresh(source)
    return source