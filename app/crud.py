from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, UserCreate
from app.security import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    result = db.execute(select(User).where(User.email == email))
    return result.scalars().first()


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_tasks(db: Session, owner_id: int) -> list[Task]:
    result = db.execute(
        select(Task).where(Task.owner_id == owner_id).order_by(Task.id)
    )
    return list(result.scalars().all())


def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Task | None:
    result = db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    )
    return result.scalars().first()


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=False,
        owner_id=owner_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, task_data: TaskUpdate) -> Task:
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    db.commit()
    db.refresh(task)
    return task


def mark_task_completed(db: Session, task: Task) -> Task:
    task.completed = True
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()