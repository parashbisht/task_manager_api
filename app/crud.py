from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def get_all_tasks(db: Session) -> list[Task]:
    result = db.execute(select(Task).order_by(Task.id))
    return list(result.scalars().all())


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    result = db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=False,
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