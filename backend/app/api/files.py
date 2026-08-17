from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.api.projects import get_owned_project
from app.database import get_db
from app.models.project import ConversionHistory, ProjectFile
from app.models.user import User
from app.schemas.project import ConversionHistoryOut, FileCreate, FileOut

router = APIRouter(prefix="/projects/{project_id}/files", tags=["files"])


async def _owned_file(
    project_id: int, file_id: int, user_id: int, db: AsyncSession
) -> ProjectFile:
    """Load a file, checking both that the caller owns the project and that the
    file belongs to it — a file_id from someone else's project must 404."""
    await get_owned_project(project_id, user_id, db)
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.id == file_id, ProjectFile.project_id == project_id
        )
    )
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.get("", response_model=list[FileOut])
async def list_files(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_project(project_id, current_user.id, db)
    result = await db.execute(
        select(ProjectFile)
        .where(ProjectFile.project_id == project_id)
        .order_by(ProjectFile.id)
    )
    return result.scalars().all()


@router.post("", response_model=FileOut, status_code=201)
async def create_file(
    project_id: int,
    data: FileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_project(project_id, current_user.id, db)
    file = ProjectFile(
        project_id=project_id,
        filename=data.filename,
        filepath=data.filepath,
        source_content=data.source_content,
        status="pending",
    )
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file


@router.get("/{file_id}", response_model=FileOut)
async def get_file(
    project_id: int,
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await _owned_file(project_id, file_id, current_user.id, db)


@router.get("/{file_id}/history", response_model=list[ConversionHistoryOut])
async def get_file_history(
    project_id: int,
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file = await _owned_file(project_id, file_id, current_user.id, db)
    result = await db.execute(
        select(ConversionHistory)
        .where(ConversionHistory.file_id == file.id)
        .order_by(ConversionHistory.version.desc())
    )
    return result.scalars().all()


@router.delete("/{file_id}")
async def delete_file(
    project_id: int,
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file = await _owned_file(project_id, file_id, current_user.id, db)
    await db.delete(file)
    await db.commit()
    return {"message": "File deleted"}
