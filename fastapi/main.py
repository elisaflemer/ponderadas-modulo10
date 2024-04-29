from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Task
import models
import database
import auth
from pydantic import BaseModel
from fastapi import Request
from fastapi import Response

app = FastAPI()

# Token authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TaskCreate(BaseModel):
    title: str
    description: str

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/api/v1/token")
async def login_for_access_token(request: Request, db: AsyncSession = Depends(database.get_db)):
    form_data = await request.json()
    user = await auth.authenticate_user(form_data["username"], form_data["password"], db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/register", response_model=UserCreate)
async def register_user(request: Request, db: AsyncSession = Depends(database.get_db)):
    user_data = await request.json()
    user = models.User(username=user_data["username"], password=user_data["password"])
    async with db as session:
        session.add(user)
        await session.commit()
    return {"message": "User created successfully", "username": user_data["username"], "password": user_data["password"]}

@app.post("/api/v1/login")
async def login(request: Request, db: AsyncSession = Depends(database.get_db)):
    form_data = await request.json()
    user = await auth.authenticate_user(form_data["username"], form_data["password"], db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print('here')
    print(dict(user))
    access_token = auth.create_access_token(user.id)
    response = JSONResponse(content={"message": "User logged in successfully"})
    response.set_cookie(key="jwt_token", value=access_token)
    return response

@app.on_event("startup")
async def startup_event():
    await models.create_tables()

@app.get("/api/v1/tasks/")
async def read_tasks(request: Request, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    # Retrieve JWT token from cookies
    token = request.cookies.get("jwt_token")
    if not token:
        raise HTTPException(status_code=401, detail="JWT token is required")

    # Authenticate user and get user_id
    user = await auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="User authentication failed")

    async with db:
        # Execute query to fetch tasks owned by the user
        result = await db.execute(select(Task).where(Task.user_id == user.id).offset(skip).limit(limit))
        tasks = result.scalars().all()

    # Assuming you have a Pydantic model for Task to serialize the database models
    tasks_data = [task.dict() for task in tasks]  # Replace this line with the appropriate serialization if needed

    # Return the serialized tasks as JSON
    return JSONResponse(content={"tasks": tasks_data})

@app.post("/api/v1/tasks/")
async def create_task(request: Request, task: TaskCreate, db: AsyncSession = Depends(database.get_db)):
    print(request.cookies)
    # Retrieve JWT token from cookies
    token = request.cookies.get("jwt_token")
    if not token:
        raise HTTPException(status_code=401, detail="No JWT token found in cookies")

    # Authenticate user and get user_id
    user = await auth.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="User authentication failed")

    # Create new task instance with user ID from the authenticated user
    new_task = Task(title=task.title, user_id=user.id)  # Assuming user object has 'id'

    # Add new task to the database
    async with db:
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)  # Refresh to get the new task with ID populated from the database

    # Return the created task as JSON
    return {"id": new_task.id, "title": new_task.title, "completed": new_task.completed, "owner_id": new_task.owner_id}

@app.put("/api/v1/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreate, request: Request, db: AsyncSession = Depends(database.get_db)):
    token = request.cookies.get("jwt_token")
    user = await auth.get_current_user(token)  # Ensure this is an async call
    if not user:
        raise HTTPException(status_code=401, detail="User authentication failed")

    async with db:
        # Ensure to check ownership by user_id which is obtained from 'user' object
        result = await db.execute(Task.update().where(
            Task.id == task_id,
            Task.user_id == user.id  # Assuming user object has an 'id' attribute
        ).values(title=task.title, description=task.description))
        await db.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found or not owned by user")
        return {"message": "Task updated successfully"}

@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    user_id = auth.get_current_user(token)
    async with db as session:
        result = await session.execute(models.Task.delete().where(models.Task.id == task_id, models.Task.user_id == user_id))
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/api/v1/tasks/")
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        result = await session.execute(models.Task.select().offset(skip).limit(limit))
        tasks = result.scalars().all()
        return tasks

@app.post("/api/v1/tasks/")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(database.get_db)):
    new_task = models.Task(title=task.title, description=task.description)
    async with db as session:
        session.add(new_task)
        await session.commit()
        return new_task

@app.put("/api/v1/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreate, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        result = await session.execute(models.Task.update().where(models.Task.id == task_id).values(title=task.title, description=task.description))
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task updated successfully"}
    
@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        result = await session.execute(models.Task.delete().where(models.Task.id == task_id))
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}

@app.on_event("startup")
async def startup_event():
    await models.create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
