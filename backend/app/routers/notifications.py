from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user

from app.models.notification import Notification
from app.models.user import User

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all notifications for the logged-in user.
    """

    notifications = (
        db.query(Notification)
        .filter(
            Notification.student_id == current_user.id
        )
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications


@router.put("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a notification as read.
    """

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.student_id == current_user.id,
        )
        .first()
    )

    if notification is None:
        return {
            "message": "Notification not found."
        }

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read.",
        "notification": notification,
    }