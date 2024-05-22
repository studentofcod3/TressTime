import uuid
from django.db import models

from appointments.models import Appointment
from users.models import CustomUser

class Notification(models.Model):
    """
    Represents messages or alerts sent to users to inform them about important events or actions
    related to their appointments or account activities.
    
    Attributes:
        id (UUIDField): A unique identifier for each notification.
        created_at (DateTimeField): The timestamp when the notification was created.
        updated_at (DateTimeField): The timestamp when the notification was last updated.
        type (CharField): The type of notification to be sent, e.g., 'email', 'sms', 'in_app'.
        status (CharField): The current status of the notification, e.g., 'pending', 'sent', 'failed'.
        subject (CharField): A title for the message, nullable.
        message (CharField): The content of the notification.
        scheduled_send_datetime (DateTimeField): The timestamp when the notification is scheduled to be sent.
        actual_sent_datetime (DateTimeField): The timestamp when the notification was sent, nullable.
        priority (CharField): The priority of the notification, e.g., 'low', 'medium', 'high'.
        channel_specific_info (JSONField): Additional information specific to the notification channel, such as email subject
            or SMS sender ID, nullable.
        response (CharField): The response received from the notification service. This can be useful for debugging any issues. 
        user (ForeignKey): A reference to the user who will receive the notification. Linked to the CustomUser model.
        appointment (ForeignKey): A reference to the appointment. Linked to the Appointment model, nullable.

    Relationships:
        - many-to-one with CustomUser
        - many-to-one with Appointment, nullable

    ## Validation
    Only database level validation should be defined in this class.
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

    # Relationships with foreign entities
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
        null=True
    )
