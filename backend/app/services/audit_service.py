from app.models.audit_log import AuditLog


def create_audit_log(
    db,
    application_id,
    action,
    performed_by,
    details="",
):
    log = AuditLog(
        application_id=application_id,
        action=action,
        performed_by=performed_by,
        details=details,
    )

    db.add(log)

    return log