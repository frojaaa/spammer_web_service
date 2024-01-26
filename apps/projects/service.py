from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .models import Project
from .schemas import ProjectCreate


class ProjectsService:
    def __init__(self, db: Session):
        self._db = db

    def get_project(self, id_: int) -> Project | None:
        return self._db.get(Project, (id_,))

    def get_projects(self, limit: int, offset: int) -> list[Project]:
        return self._db.query(Project).offset(offset).limit(limit).all()

    def create_projects(self, projects: set[ProjectCreate]) -> list[Project]:
        instances = [project.model_dump() for project in projects]
        instances = self._db.scalars(insert(Project).on_conflict_do_nothing().returning(Project), instances)
        self._db.commit()
        return instances

    def delete_project(self, id_: int) -> None:
        self._db.query(Project).filter(Project.id == id_).delete()
        self._db.commit()

    def edit_project(self, project: ProjectCreate) -> Project | None:
        proj = self._db.get(Project, (project.id,))
        if proj:
            proj.message = project.message
            proj.name = project.name
            self._db.add(proj)
            self._db.commit()
            self._db.refresh(proj)
            return proj
