import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    """
    The Service model represents the different services offered by the hairdressing business, such as haircuts, coloring,
    and treatments.

    Attributes:
        id (UUIDField): A unique identifier for each service.
        created_at (DateTimeField): The timestamp when the service was created.
        updated_at (DateTimeField): The timestamp when the service was last updated.
        name (CharField): The name/title of the service. Should be descriptive and recognizable.
        description (TextField): A detailed description of what the service involves.
            Helps users understand what the service includes and its benefits.
        duration (DurationField): The typical length of time the service takes to complete. 
            Measured in minutes, crucial for scheduling appointments.
        price (DecimalField): The price of the service (In GBP). Important for billing and financial transactions.
        availability (BooleanField): Indicates whether the service is currently available for booking. 
            Helps manage seasonal offerings or services that are temporarily unavailable.
        image (ImageField): Image representing the service. Enhances user engagement and helps in visually 
            identifying the service.
        minimum_notice (IntegerField): The minimum notice period required to book the service. Measured in hours, 
            crucial for managing last minute bookings.

        
    Relationships:
        - one-to-many with Appointments (Relationship defined in Appointment data model)

    ## Validation
    Only database level validation should be defined in this class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    name = models.CharField(
        default=None,
        max_length=150,
        null=False,
        unique=True,
    )
    description = models.CharField(
        default=None,
        max_length=2000,
        null=False,
    )
    duration = models.IntegerField(null=False)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=False,
    )
    availability = models.BooleanField(default=True, null=False)
    # Used ImageField as opposed to URLField as we want to ensure control, security, and a seamless user experience.
    image = models.ImageField(
        upload_to='service_images/',
        null=True,
    )
    minimum_notice = models.IntegerField(null=True)
