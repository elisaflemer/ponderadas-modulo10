from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from database import get_session, engine, Base
from models.tasks import Task
import json

async def get_tasks_by_user(session: AsyncSession, user_id: int):
    stmt = select(Task).filter(Task.user_id == user_id).options(selectinload(Task.user))
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return [task.to_dict() for task in tasks]

async def get_task_by_id(session, task_id: int, user_id: int):
    stmt = select(Task).filter(Task.id == task_id and Task.user_id == user_id).options(selectinload(Task.user))
    result = await session.execute(stmt)
    task = result.scalar()
    return task.to_dict() if task else None

async def create_task(session, title: str, user_id: int):
    task = Task(title=title, user_id=user_id)
    session.add(task)
    await session.commit()
    return {'id': task.id, 'title': task.title, 'status': task.status, 'created_at': task.created_at.isoformat() if task.created_at else None, 'updated_at': task.updated_at.isoformat() if task.updated_at else None}

async def update_task(session, task_id: int, title: str, user_id: int):
    stmt = select(Task).filter(Task.id == task_id and Task.user_id == user_id).options(selectinload(Task.user))
    result = await session.execute(stmt)
    task = result.scalar()
    if not task:
        return None
    task.title = title
    await session.commit()
    return task.to_dict()

async def delete_task(session, task_id: int, user_id: int):
    stmt = select(Task).filter(Task.id == task_id and Task.user_id == user_id). options(selectinload(Task.user))
    result = await session.execute(stmt)
    task = result.scalar()
    if not task:
        return None
    session.delete(task)
    await session.commit()
    return task.to_dict()


