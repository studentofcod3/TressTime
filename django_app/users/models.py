import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Represents individuals who interact with the application. This includes staff, customers and admins.

    ## Place withing the system
    Core component. Has a central role in user management, authentication and authorization within the application.

    Relationships:
    - one-to-many with Appointment
    - one-to-many with Notification
    - one-to-many with PaymentDetails
    - one-to-many with PaymentMethod
    - one-to-many with BillingAddress

    ## Validation
    Although some of the fields are used at the form level (which will require validation),
    we need to ensure that we do not violate any of the SOLID principles. Therefore, a decision has been made to
    only enforce database level validation (ie: 'null' property), and not utilise django's
    built in form level validation (ie: required/blank). This is the same across all data models.

    ## Override information
    The name CustomUser is defined so as not to clash with Django's built-in User model.

    Most of the needed fields are covered by AbstractUser, with only some minor adjustments. The list below contains
    information on which inherited fields are currently utilised in this project:

    username - overridden (definition: AbstractUser)
    email - overridden (definition: AbstractBaseUser)
    password - overridden (definition: AbstractBaseUser)
    first_name - full coverage (definition: AbstractUser)
    last_name - full coverage (definition: AbstractUser)
    date_joined - full coverage, technically a datetime field (definition: AbstractUser)
    last_login - full coverage, technically a datetime field (definition: AbstractBaseUser)
    is_active - full coverage (definition: AbstractUser)
    is_staff - full coverage (definition: AbstractUser)
    is_superuser - full coverage (definition PermissionsMixin)
    """

    # TODO: The logic for preventing editing of id will be addressed when implementing the repository pattern
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # TODO:
    #  The logic for handling `created_at` and `updated_at` will be addressed when implementing
    #  the repository pattern. At that point the auto_now_add and auto_now properties are to be removed.
    #  They are currently only kept so the that the initial automated tests can run on the model and provide
    #  some degree of coverage.
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # Used ImageField as opposed to URLField as we want to ensure control, security, and a seamless user experience.
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
    )

    # Fields below are overrides to AbstractUser fields to change their properties.
    # Only database-level overrides are defined here.
    username = models.CharField(
        default=None,
        unique=True
    )
    email = models.EmailField(
        default=None,
        unique=True,
        null=False,
    )
    password = models.CharField(default=None)

    # Modify the related_name for each many-to-many field. Due to inheritance, This is needed to avoid conflicts
    # with the AbstractUser related_names which must be unique.
    groups = models.ManyToManyField(
        to='auth.Group',
        related_name="custom_user_set",  # Unique related_name
        related_query_name="custom_user",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        to='auth.Permission',
        related_name="custom_user_permissions_set",  # Unique related_name
        related_query_name="custom_user_permission",
        blank=True
    )



