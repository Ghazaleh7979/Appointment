from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    class EventType(models.TextChoices):
        LOGIN_SUCCESS = "LOGIN_SUCCESS", "Login Success"
        LOGIN_FAILED = "LOGIN_FAILED", "Login Failed"
        LOGOUT = "LOGOUT", "Logout"
        PASSWORD_RESET_REQUEST = "PASSWORD_RESET_REQUEST", "Password Reset Request"
        PASSWORD_RESET_SUCCESS = "PASSWORD_RESET_SUCCESS", "Password Reset Success"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    event_type = models.CharField(
        max_length=50,
        choices=EventType.choices,
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
