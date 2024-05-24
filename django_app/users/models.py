import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Represents individuals who interact with the application.

    This includes customers who book services, as well as staff and administrators who manage the system.
    
    Most of the needed fields are covered by AbstractUser, with only some minor adjustments. 
    The name 'CustomUser' is used so as not to clash with Django's built-in User model.

    Attributes (Includes inherited fields currently utilised in this project):
        id (UUIDField): A unique identifier for each user.
        created_at (DateTimeField): The timestamp when the user was created.
        updated_at (DateTimeField): The timestamp when the user was last updated.
        username (CharField): The unique username of the user (override declared here - original definition in AbstractUser).
        email (EmailField): The email address of the user (override declared here - original definition in AbstractBaseUser).
        password (CharField): The hashed password of the user (override declared here - original definition in AbstractBaseUser).
        first_name (CharField): The first name of the user (original definition in AbstractUser).
        last_name (CharField): The last name of the user (original definition in AbstractUser).
        date_joined (DateTimeField): The date and time when the user registered (original definition in AbstractUser).
        last_login (DateTimeField): The date and time of the user's last login (original definition in AbstractBaseUser).
        profile_picture (ImageField): An optional profile picture for the user.
        is_staff (BooleanField): Whether the user can access the admin site (original definition in AbstractUser).
        is_active (BooleanField): Whether the user's account is active (original definition in AbstractUser).
        is_superuser (BooleanField): Whether the user's account has all permissions (original definition in PermissionsMixin).

    Relationships:
        - one-to-many with Appointment (Relationship defined in Appointment data model)
        - one-to-many with Notification (Relationship defined in Notification data model)
        - many-to-many with Group (override declared here)
        - many-to-many with Permission (override declared here)

    ## Validation
    Although some of the fields are used at the form level (which will require validation),
    we need to ensure that we do not violate any of the SOLID principles. Therefore, a decision has been made to
    only enforce database level validation (ie: 'null' property), and not utilise django's
    built in form level validation (ie: required/blank). This is the same across all data models.
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



