from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from fastapi import status
from loguru import logger

from apps.projects.schemas import ProjectCreate, ProjectEdit, Project


@pytest.mark.asyncio
async def test_get_projects(client: TestClient):
    response = await client.get('/projects')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_read_project(client: TestClient):
    response = await client.get('/projects/0')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_projects(client: TestClient):
    project = ProjectCreate(name='test', message='test_message')
    response = await client.post("/projects/create", json=[project.model_dump()])
    assert response.status_code == status.HTTP_201_CREATED and len(response.json()) > 0
    logger.debug(response.json())
    project = Project.model_validate(response.json()[0])
    response = await client.get(f"/projects/{project.id}")
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(f"/projects/{project.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await client.get(f"/projects/{project.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_edit_project(client: TestClient):
    project = ProjectEdit(id=0, name='string', message=f'test_message @ {datetime.now().isoformat()}')
    response = await client.put(f"/projects/{project.id}", json=project.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == project.message
