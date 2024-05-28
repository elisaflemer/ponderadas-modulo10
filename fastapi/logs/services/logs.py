from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from database import get_session, engine, Base
from models.logs import Log
import json


async def create_log(session, message: str, level: str, user: str):
    log = Log(message=message, level=level, user=user)
    session.add(log)
    await session.commit()
    return {'id': log.id, 'message': log.message, 'level': log.level, 'created_at': log.created_at.isoformat() if log.created_at else None}

async def get_all_logs(session):
    stmt = select(Log)
    result = await session.execute(stmt)
    logs = result.scalars().all()
    return [log.to_dict() for log in logs]
