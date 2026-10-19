from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import DataResponse
from app.schemas.task_source import TaskSourceCreate, TaskSourceRead
from app.services import task_source_service
from database import get_db

router = APIRouter(prefix="/api/v1/task-sources", tags=["task sources"])


@router.post("", response_model=DataResponse[TaskSourceRead], status_code=201)
def create_task_source(
    payload: TaskSourceCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    source = task_source_service.create_source(db, user, payload)
    return {"data": source}