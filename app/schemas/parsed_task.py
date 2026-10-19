from pydantic import BaseModel, Field


class ParsedTask(BaseModel):
    task_title: str = Field(description="Short, actionable title")
    task_description: str | None = Field(default=None, description="Extra detail, if any")
    category: str | None = Field(default=None, description="One word, e.g. work, home, study")
    due_date: str | None = Field(
        default=None, description="Due date as ISO 8601 (YYYY-MM-DD), only if stated or clearly implied"
    )
    estimated_minutes: int | None = Field(default=None, description="Rough effort estimate")


class ParsedTaskList(BaseModel):
    tasks: list[ParsedTask]