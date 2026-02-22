# app/demo/routes.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from app.users.models import User
from app.auth.validation import get_current_active_user_with_permissions
from app.users.exception_handler import handle_user_errors
from .service import DemoService
from .models import Project, Task, Document


router = APIRouter(prefix="/demo", tags=["demo"])


def get_demo_service(
    current_user: User = Depends(get_current_active_user_with_permissions),
) -> DemoService:
    return DemoService(current_user)


@router.get("/projects", response_model=List[Project])
@handle_user_errors
async def get_projects(service: DemoService = Depends(get_demo_service)):
    return service.get_projects()


@router.get("/projects/{project_id}", response_model=Project)
@handle_user_errors
async def get_project(
    project_id: int, service: DemoService = Depends(get_demo_service)
):
    return service.get_project(project_id)


@router.patch("/projects/{project_id}", response_model=Project)
@handle_user_errors
async def update_project(
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    service: DemoService = Depends(get_demo_service),
):
    return service.update_project(project_id, name=name, description=description)


@router.get("/tasks", response_model=List[Task])
@handle_user_errors
async def get_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project"),
    service: DemoService = Depends(get_demo_service),
):
    return service.get_tasks(project_id)


@router.get("/tasks/{task_id}", response_model=Task)
@handle_user_errors
async def get_task(task_id: int, service: DemoService = Depends(get_demo_service)):
    return service.get_task(task_id)


@router.patch("/tasks/{task_id}", response_model=Task)
@handle_user_errors
async def update_task(
    task_id: int,
    title: Optional[str] = None,
    assignee_id: Optional[int] = None,
    service: DemoService = Depends(get_demo_service),
):
    return service.update_task(task_id, title=title, assignee_id=assignee_id)


@router.get("/documents", response_model=List[Document])
@handle_user_errors
async def get_documents(
    project_id: Optional[int] = Query(None, description="Filter by project"),
    service: DemoService = Depends(get_demo_service),
):
    return service.get_documents(project_id)


@router.get("/documents/{document_id}", response_model=Document)
@handle_user_errors
async def get_document(
    document_id: int, service: DemoService = Depends(get_demo_service)
):
    return service.get_document(document_id)
