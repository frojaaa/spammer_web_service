from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

from .service import ProjectsService
from .schemas import Project, ProjectCreate, ProjectEdit
from db import SessionLocal
from ..dependencies import common_parameters
from ..schemas import CommonParams

router = APIRouter(prefix='/projects', tags=['projects'], responses={404: {"description": "Not found"}})
CommonsDep = Annotated[CommonParams, Depends(common_parameters)]


def get_projects_service() -> ProjectsService:
    db = SessionLocal()
    service = ProjectsService(db)
    try:
        yield service
    finally:
        db.close()


@router.get('/', response_model=list[Project])
def read_projects(
        commons: CommonsDep,
        service: ProjectsService = Depends(get_projects_service)
) -> list[Project]:
    projects = service.get_projects(commons.limit, commons.offset)
    return projects


@router.get('/{project_id}', response_model=Project)
def read_project(project_id: int, service: ProjectsService = Depends(get_projects_service)):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, service: ProjectsService = Depends(get_projects_service)):
    service.delete_project(project_id)


@router.put('/{project_id}', response_model=Project, status_code=status.HTTP_201_CREATED)
def update_project(project_id: int, project: ProjectEdit, service: ProjectsService = Depends(get_projects_service)):
    acc = service.get_project(project_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Project not found")
    acc = service.edit_project(project)
    return acc


@router.post('/create', response_model=list[Project], status_code=status.HTTP_201_CREATED)
def create_projects(projects: set[ProjectCreate], service: ProjectsService = Depends(get_projects_service)):
    return service.create_projects(projects)
