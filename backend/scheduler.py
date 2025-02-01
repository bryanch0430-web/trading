from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from .database import SessionLocal
from .model import ValueHistory, User, UserAsset
from datetime import datetime
from pytz import timezone
from sqlalchemy import func
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_user_total_value(user: User, db: Session) -> float:

    total = db.query(func.sum(UserAsset.total_value)).filter(UserAsset.user_id == user.id).scalar()
    return total or 0.0

def save_daily_value_history():
    logger.info("Starting daily value history job.")
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()

        
        for user in users:
            total_value = calculate_user_total_value(user, db)
            value_history = ValueHistory(
                user_id=user.id,
                total_value=total_value,
                timestamp=datetime.now(timezone('Asia/Hong_Kong')).replace(hour=0, minute=0, second=0, microsecond=0)
            )
            db.add(value_history)
        db.commit()
        logger.info("Successfully saved daily value history.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving daily value history: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler(timezone='Asia/Hong_Kong')
    trigger = CronTrigger(hour=0, minute=0)  
    scheduler.add_job(save_daily_value_history, trigger, name="DailyValueHistoryJob")

    scheduler.start()
    logger.info("Scheduler started and job added.")