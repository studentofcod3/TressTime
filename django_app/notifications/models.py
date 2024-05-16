import uuid
from django.db import models

from appointments.models import Appointment
from users.models import CustomUser

class Notification(models.Model):
    """
    Represents messages or alerts sent to users to inform them about important events or actions.
    
    The events are related to the users' appointments or account activities. 
    These notifications can be sent via various channels, such as email, SMS, or in-app messages.

    This is a core component of the user communication system. It ensures users are informed about 
    their bookings, reminders, cancellations, and any important updates related to their accounts 
    or services.

    Relationships:
    - many-to-one with User
    - many-to-one with appointment
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    type = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=20, null=False)
    subject = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=500, null=False)
    scheduled_send_datetime = models.DateTimeField(null=False)
    actual_sent_datetime = models.DateTimeField(null=True)
    priority = models.CharField(max_length=20, null=False)
    channel_specific_info = models.JSONField(null=True)
    response =  models.CharField(max_length=500, null=True)

    # Relationships with foreing entities
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='notifications',
        null=False
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.PROTECT,
        related_name='notifications',
        null=False
    )
