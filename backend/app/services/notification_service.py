from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.student import Student


def create_notification(
    db: Session,
    student: Student,
    title: str,
    message: str,
    notification_type: str = "System",
):
    """
    Create a notification for a student.
    """

    notification = Notification(
        student_id=student.id,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification