from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from models import User, Task
import models
import database
import auth
from pydantic import BaseModel
from fastapi import Request
from fastapi import Response

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

@app.get("/api/v1/tasks")
async def read_tasks(request: Request, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    # Retrieve JWT token from cookies
   
    async with db:
        # Execute query to fetch tasks owned by the user
        result = await db.execute(select(Task).offset(skip).limit(limit))
        tasks = result.scalars().all()

    # Assuming you have a Pydantic model for Task to serialize the database models
    tasks_data = [{"id": task.id, "title": task.title, "completed": task.completed} for task in tasks]

    # Return the serialized tasks as JSON
    return JSONResponse(content={"tasks": tasks_data})

@app.post("/api/v1/tasks")
async def create_task(request: Request, task: TaskCreate, db: AsyncSession = Depends(database.get_db)):
   
    # Create new task instance with user ID from the authenticated user
    new_task = Task(title=task.title)  # Assuming user object has 'id'

    print(new_task)

    # Add new task to the database
    async with db:
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)  # Refresh to get the new task with ID populated from the database

    # Return the created task as JSON
    return {"id": new_task.id, "title": new_task.title, "completed": new_task.completed}

@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: int, request: Request, db: AsyncSession = Depends(database.get_db)):
  
    async with db:
        # Attempt to delete the task
        result = await db.execute(delete(models.Task).where(
            models.Task.id == task_id, 
        ))
        await db.commit()

        # Check if any row was affected
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {"message": "Task deleted successfully"}
    
@app.put("/api/v1/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreate, request: Request, db: AsyncSession = Depends(database.get_db)):
    
    async with db:
        # Fetch the task by ID
        result = await db.execute(select(models.Task).where(models.Task.id == task_id))
        task = result.scalars().first()

        # Check if task exists
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update the task with the new title
        task.title = task.title
        await db.commit()

        # Return the updated task as JSON
        return {"id": task.id, "title": task.title, "completed": task.completed}
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.on_event("startup")
async def startup_event():
    await models.create_tables()
