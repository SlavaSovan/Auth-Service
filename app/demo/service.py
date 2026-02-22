from typing import List, Optional
from fastapi import HTTPException, status

from app.users.models import User
from .models import mock_projects, mock_tasks, mock_documents, Project, Task, Document


class DemoService:
    def __init__(self, current_user: User):
        self.user = current_user
        self.user_permissions = {perm.name for perm in current_user.role.permissions}

    def _has_permission(self, permission: str) -> bool:
        """Проверка наличия права"""
        return permission in self.user_permissions

    def get_projects(self) -> List[Project]:
        """Получить проекты в зависимости от прав"""
        if self._has_permission("project:read:any"):
            return list(mock_projects.values())
        elif self._has_permission("project:read:own"):
            return [p for p in mock_projects.values() if p.owner_id == self.user.id]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view projects",
        )

    def get_project(self, project_id: int) -> Project:
        """Получить проект по ID"""
        project = mock_projects.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        if self._has_permission("project:read:any"):
            return project
        elif (
            self._has_permission("project:read:own")
            and project.owner_id == self.user.id
        ):
            return project
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this project",
        )

    def update_project(self, project_id: int, **data) -> Project:
        """Обновить проект"""
        project = self.get_project(project_id)

        if self._has_permission("project:write:any"):
            pass
        elif (
            self._has_permission("project:write:own")
            and project.owner_id == self.user.id
        ):
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to edit this project",
            )

        for key, value in data.items():
            if hasattr(project, key) and value is not None:
                setattr(project, key, value)

        return project

    def get_tasks(self, project_id: Optional[int] = None) -> List[Task]:
        """Получить задачи"""
        tasks = mock_tasks.values()
        if project_id:
            tasks = [t for t in tasks if t.project_id == project_id]

        if self._has_permission("task:read:any"):
            return list(tasks)
        elif self._has_permission("task:read:own"):
            return [
                t
                for t in tasks
                if t.assignee_id == self.user.id or t.creator_id == self.user.id
            ]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view tasks",
        )

    def get_task(self, task_id: int) -> Task:
        """Получить задачу по ID"""
        task = mock_tasks.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        if self._has_permission("task:read:any"):
            return task
        elif self._has_permission("task:read:own") and (
            task.assignee_id == self.user.id or task.creator_id == self.user.id
        ):
            return task
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view task",
        )

    def update_task(self, task_id: int, **data) -> Task:
        """Обновить задачу"""
        task = self.get_task(task_id)

        if self._has_permission("task:write:any"):
            pass
        elif self._has_permission("task:write:own") and (
            task.assignee_id == self.user.id or task.creator_id == self.user.id
        ):
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to edit this task",
            )

        for key, value in data.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)

        return task

    def get_documents(self, project_id: Optional[int] = None) -> List[Document]:
        """Получить документы"""
        docs = mock_documents.values()
        if project_id:
            docs = [d for d in docs if d.project_id == project_id]

        if self._has_permission("document:read:any"):
            return list(docs)
        elif self._has_permission("document:read:own"):
            return [d for d in docs if d.uploader_id == self.user.id]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view documents",
        )

    def get_document(self, document_id: int) -> Document:
        """Получить документ по ID"""
        doc = mock_documents.get(document_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
            )

        if self._has_permission("document:read:any"):
            return doc
        elif (
            self._has_permission("document:read:own")
            and doc.uploader_id == self.user.id
        ):
            return doc

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this document",
        )
