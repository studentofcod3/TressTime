import uuid

from django.db import models

from services.models import Service
from users.models import CustomUser


class Appointment(models.Model):
    """
    Represents a scheduled appointment for a service provided by the hairdressing business.

    Attributes:
        id (UUIDField): A unique identifier for each appointment.
        created_at (DateTimeField): The timestamp when the appointment was created.
        updated_at (DateTimeField): The timestamp when the appointment was last updated.
        starts_at (DateTimeField): The date and time when the appointment is scheduled to take begin.
        ends_at (DateTimeField): The date and time when the appointment is scheduled to take end.
        status (CharField): The current status of the appointment, e.g., 'scheduled', 'completed', 'canceled'.
        confirmation_number: A unique confirmation code sent to customers, e.g, for tracking appointments, verifying bookings etc.
        notes (CharField): Optional notes or special instructions related to the appointment.
        user (ForeignKey): A reference to the user who booked the appointment. Linked to the CustomUser model.
        service (ForeignKey): A reference to the service that has been booked for the appointment. Linked to the Service model.

    Relationships:
        - many-to-one with User
        - many-to-one with Service
        - one-to-many with Notification (Relationship defined in Notification data model)

    ## Validation
    Only database level validation should be defined in this class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    starts_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=False)
    status = models.CharField(max_length=20, null=False)
    confirmation_number = models.IntegerField(unique=True, null=True)
    notes = models.CharField(max_length=200, null=True)

    # Relationships with foreign entities
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='appointments',
        null=False
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments',
        null=False
    )


