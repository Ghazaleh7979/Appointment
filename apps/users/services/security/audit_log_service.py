from apps.users.models import AuditLog


def create_audit_log(
    *,
    user=None,
    event_type: str,
    ip_address: str | None = None,
    user_agent: str | None = "",
    metadata: dict | None = None,
):
    AuditLog.objects.create(
        user=user,
        event_type=event_type,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata or {},
    )
