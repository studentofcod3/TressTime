import uuid

from django.db import models

from services.models import Service
from users.models import CustomUser


class Appointment(models.Model):
    """
    Represents bookings made by users for services.

    ## Place within the system
    Core Component. Fundamental to the core buses logic of the hairdressing booking system.

    Relationships:
    - many-to-one with user
    - many-to-one with service
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


