from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, validator
from enum import Enum
 
import database
 
database.Base.metadata.create_all(bind=database.engine)
 
app = FastAPI()
 
# Pydantic schemas
 
class Status(str, Enum):
    pending = "pending"
    completed = "completed"
 
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
 
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status = Status.pending
    due_date: Optional[date] = None
    priority: Priority = Priority.medium
 
    @validator('due_date')
    def due_date_cannot_be_past(cls, v):
        if v and v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v
 
class TaskCreate(TaskBase):
    pass
 
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    due_date: Optional[date] = None
    priority: Optional[Priority] = None
 
    @validator('due_date')
    def due_date_cannot_be_past(cls, v):
        if v and v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v
 
class Task(TaskBase):
    id: int
    created_at: datetime
 
    class Config:
        from_attributes = True
 
# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
# CRUD operations
 
@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = database.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
 
@app.get("/tasks/", response_model=List[Task])
def read_tasks(
    status: Optional[Status] = None,
    due_date: Optional[date] = None,
    priority: Optional[Priority] = None,
    db: Session = Depends(get_db)
):
    query = db.query(database.Task)
    if status:
        query = query.filter(database.Task.status == status)
    if due_date:
        query = query.filter(database.Task.due_date == due_date)
    if priority:
        query = query.filter(database.Task.priority == priority)
    return query.all()
 
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
 
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
 
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
 
    db.commit()
    db.refresh(task)
    return task
 
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return




 
