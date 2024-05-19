from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from database import get_session, engine, Base
from models.logs import Log
import json

async def get_logs_by_user(session: AsyncSession, user_id: int):
    stmt = select(Log).filter(Log.user_id == user_id)
    result = await session.execute(stmt)
    logs = result.scalars().all()
    return [log.to_dict() for log in logs]

async def get_log_by_id(session, log_id: int, user_id: int):
    stmt = select(Log).filter(Log.id == log_id and Log.user_id == user_id)
    result = await session.execute(stmt)
    log = result.scalar()
    return log.to_dict() if log else None

async def create_log(session, message: str, level: str, user_id: int):
    log = Log(message=message, level=level, user_id=user_id)
    session.add(log)
    await session.commit()
    return {'id': log.id, 'message': log.message, 'level': log.level, 'created_at': log.created_at.isoformat() if log.created_at else None}
