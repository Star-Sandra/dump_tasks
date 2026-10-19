from sqlalchemy.orm import Session

from app.models.task_source import TaskSource
from app.models.user import User
from app.repositories import task_source_repository
from app.schemas.task_source import TaskSourceCreate


def create_source(db: Session, user: User, data: TaskSourceCreate) -> TaskSource:
    raw_input = data.raw_input.strip()
    return task_source_repository.create(db, user.user_id, data.input_type, raw_input)