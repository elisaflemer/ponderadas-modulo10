from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import hash_password, create_access_token, verify_password, get_current_user
from services.tasks import get_tasks_by_user, get_task_by_id, create_task, update_task, delete_task
from database import get_session  # make sure to have this function defined in your database module
from models.schemas import UserRegistrationRequest, UserResponseModel, LoginResponseModel, UserLoginRequest, TaskRequest

router = APIRouter(prefix="/tasks")

@router.get("/")
async def get_tasks( session = Depends(get_session), user = Depends(get_current_user)):
    tasks = await get_tasks_by_user(session, user['id'])
    return tasks

@router.get("/{task_id}")
async def get_task(task_id: int, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    task = await get_task_by_id(session, task_id, user['id'])
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/")
async def create_new_task(request: TaskRequest, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    task = await create_task(session, request.title, user['id'])
    return task

@router.put("/{task_id}")
async def update_existing_task(task_id: int, title: str, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    task = await update_task(session, task_id, title, user['id'])
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_existing_task(task_id: int, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    task = await delete_task(session, task_id, user['id'])
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task