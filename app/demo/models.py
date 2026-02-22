from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime


class Task(BaseModel):
    id: int
    title: str
    project_id: int
    assignee_id: Optional[int] = None
    creator_id: int
    created_at: datetime


class Document(BaseModel):
    id: int
    filename: str
    project_id: int
    uploader_id: int
    created_at: datetime


mock_projects = {
    1: Project(
        id=1,
        name="Project 1",
        description="First project",
        owner_id=1,
        created_at=datetime.now(),
    ),
    2: Project(
        id=2,
        name="Project 2",
        description="Second project",
        owner_id=2,
        created_at=datetime.now(),
    ),
}

mock_tasks = {
    1: Task(
        id=1,
        title="Task 1",
        project_id=1,
        assignee_id=1,
        creator_id=1,
        created_at=datetime.now(),
    ),
    2: Task(
        id=2,
        title="Task 2",
        project_id=1,
        assignee_id=1,
        creator_id=2,
        created_at=datetime.now(),
    ),
    3: Task(
        id=3,
        title="Task 3",
        project_id=2,
        assignee_id=4,
        creator_id=2,
        created_at=datetime.now(),
    ),
}

mock_documents = {
    1: Document(
        id=1,
        filename="doc1.pdf",
        project_id=1,
        uploader_id=1,
        created_at=datetime.now(),
    ),
    2: Document(
        id=2,
        filename="doc2.pdf",
        project_id=2,
        uploader_id=3,
        created_at=datetime.now(),
    ),
    3: Document(
        id=3,
        filename="doc3.pdf",
        project_id=2,
        uploader_id=5,
        created_at=datetime.now(),
    ),
}
