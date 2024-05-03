import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    """
    Represents the services available for booking.

    ## Place within the system
    Core Component. Services form the foundation of the booking system and are essential for users to interact
    with the platform.

    Relationships:
    - one-to-many with Appointments (Relationship defined in Service data model)

    ## Validation
    Only database level validation should be defined in this class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # The name/title of the service. Should be descriptive and recognizable.
    name = models.CharField(
        default=None,
        max_length=150,
        null=False,
        unique=True,
    )
    # A detailed description of what the service involves.
    # Helps users understand what the service includes and its benefits.
    description = models.CharField(
        default=None,
        max_length=2000,
        null=False,
    )
    # The length of time the service takes to complete. Measured in minutes, crucial for scheduling appointments.
    duration = models.IntegerField(null=False)
    # The cost of availing the service (In GBP). Important for billing and financial transactions.
    price = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=False,
    )
    # Indicates whether the service is currently available for booking.
    # Helps manage seasonal offerings or services that are temporarily unavailable.
    availability = models.BooleanField(default=True, null=False)
    # Image representing the service. Enhances user engagement and helps in visually identifying the service.
    # Used ImageField as opposed to URLField as we want to ensure control, security, and a seamless user experience.
    image = models.ImageField(
        upload_to='service_images/',
        null=True,
    )
    # The minimum notice period required to book the service.
    # Measured in hours, crucial for managing last minute bookings.
    minimum_notice = models.IntegerField(null=True)
