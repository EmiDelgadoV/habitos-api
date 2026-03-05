from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app import models, schemas
from app.auth.utils import get_current_user

router = APIRouter(prefix="/habits", tags=["Hábitos"])

@router.post("/", response_model=schemas.HabitResponse, status_code=201)
def create_habit(
    habit_data: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_habit = models.Habit(
        name=habit_data.name,
        description=habit_data.description,
        owner_id=current_user.id
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@router.get("/", response_model=list[schemas.HabitResponse])
def get_habits(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    habits = db.query(models.Habit).filter(
        models.Habit.owner_id == current_user.id
    ).all()
    return habits

@router.put("/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(
    habit_id: int,
    habit_data: schemas.HabitUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")

    if habit_data.name is not None:
        habit.name = habit_data.name
    if habit_data.description is not None:
        habit.description = habit_data.description

    db.commit()
    db.refresh(habit)
    return habit

@router.delete("/{habit_id}", status_code=204)
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")

    db.delete(habit)
    db.commit()

@router.post("/{habit_id}/log", response_model=schemas.HabitLogResponse, status_code=201)
def log_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")

    today = date.today()
    existing_log = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit_id,
        models.HabitLog.date == today
    ).first()
    if existing_log:
        raise HTTPException(status_code=400, detail="Ya completaste este hábito hoy")

    log = models.HabitLog(habit_id=habit_id, date=today, completed=True)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/{habit_id}/history")
def get_history(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")

    logs = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit_id
    ).order_by(models.HabitLog.date.desc()).all()

    streak = 0
    check_date = date.today()
    log_dates = {log.date for log in logs}

    while check_date in log_dates:
        streak += 1
        check_date = check_date.replace(day=check_date.day - 1)

    return {
        "habit_id": habit_id,
        "total_completions": len(logs),
        "current_streak": streak,
        "logs": [{"date": str(log.date), "completed": log.completed} for log in logs]
    }