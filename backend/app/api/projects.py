from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.database import get_db
from app.models.project import Project, ProjectFile
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def _to_out(project: Project, file_count: int) -> ProjectOut:
    out = ProjectOut.model_validate(project)
    out.file_count = file_count
    return out


async def get_owned_project(project_id: int, user_id: int, db: AsyncSession) -> Project:
    """Load a project the caller owns, or 404. Never leaks another user's rows."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == user_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def _file_count(project_id: int, db: AsyncSession) -> int:
    result = await db.execute(
        select(func.count(ProjectFile.id)).where(ProjectFile.project_id == project_id)
    )
    return result.scalar() or 0


@router.get("", response_model=list[ProjectOut])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # One grouped query rather than a COUNT per project.
    result = await db.execute(
        select(Project, func.count(ProjectFile.id))
        .outerjoin(ProjectFile, ProjectFile.project_id == Project.id)
        .where(Project.user_id == current_user.id)
        .group_by(Project.id)
        .order_by(Project.updated_at.desc())
    )
    return [_to_out(project, count) for project, count in result.all()]


@router.post("", response_model=ProjectOut, status_code=201)
async def create_project(
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = Project(**data.model_dump(), user_id=current_user.id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return _to_out(project, 0)


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await get_owned_project(project_id, current_user.id, db)
    return _to_out(project, await _file_count(project_id, db))


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await get_owned_project(project_id, current_user.id, db)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return _to_out(project, await _file_count(project_id, db))


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await get_owned_project(project_id, current_user.id, db)
    await db.delete(project)
    await db.commit()
    return {"message": "Project deleted"}
