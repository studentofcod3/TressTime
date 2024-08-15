import re

from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

class UserServiceValidator:
    """
    Validates the business logic for the User entity.

    Methods:
        validate_user_data(user_data, is_update=False)
        validate_created_at(created_at)
        validate_updated_at(updated_at)
        validate_name(name)
        validate_description(description)
        validate_price(price)
        validate_duration(duration)
        validate_category(category)
        validate_created_at(created_at)
        validate_updated_at(updated_at)
    """

    ALLOWED_EMAIL_DOMAINS = ["gmail.com", "test.com"]
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

    def validate_user_exists(self, user, user_id):
        if not user:
            raise ValidationError(f"User with ID {user_id} does not exist.")
        
    def validate_user_data(self, user_data, is_update=False):
        """
        Validates user data.
        
        This contains any business logic validation (e.g., string length, value ranges, format checks).
        Any database level constraints (e.g., unique constraints, field types, nullability) should be defined on the model.
        """
        if is_update:
            if 'id' in user_data:
                raise ValidationError("ID cannot be modified.")
            self.validate_updated_at(user_data.get('updated_at', None))
        else:
            self.validate_created_at(user_data.get('created_at', None))
            self.validate_updated_at(user_data.get('updated_at', None))
        self.validate_username(user_data.get('username', None), is_update)
        self.validate_email(user_data.get('email', None), is_update)
        self.validate_password(user_data.get('password', None), is_update)
        self.validate_first_name(user_data.get('first_name', None))
        self.validate_last_name(user_data.get('last_name', None))
        self.validate_profile_picture(user_data.get('profile_picture', None))
    
    def validate_created_at(self, created_at):
        """
        Validates the created_at timestamp.
        Args:
            created_at (datetime): The created_at timestamp to validate.
        Raises:
            ValidationError: If the created_at timestamp is invalid.
        """
        if created_at is None:
            raise ValidationError("created_at is required.")
        if not isinstance(created_at, datetime):
            raise ValidationError("created_at must be a datetime object.")
        if created_at.tzinfo is None or created_at.tzinfo.utcoffset(created_at) is None:
            raise ValidationError("created_at must be an aware datetime object with timezone information.")

    def validate_updated_at(self, updated_at):
        """
        Validates the updated_at timestamp.
        Args:
            updated_at (datetime): The updated_at timestamp to validate.
        Raises:
            ValidationError: If the updated_at timestamp is invalid.
        """
        if updated_at is None:
            raise ValidationError("updated_at is required.")
        if not isinstance(updated_at, datetime):
            raise ValidationError("updated_at must be a datetime object.")
        if updated_at.tzinfo is None or updated_at.tzinfo.utcoffset(updated_at) is None:
            raise ValidationError("updated_at must be an aware datetime object with timezone information.")
        
    def validate_username(self, username, is_update=False):
        """Ensure the username meets the minimum length."""
        if not username and not is_update:
            raise ValidationError("username is required.")
        if not username and is_update:
            return
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
    
    def validate_email(self, email, is_update=False):
        """Ensure that the submission is an email and that the email domain is whitelisted."""
        if not email and not is_update:
            raise ValidationError("email is required.")
        if not email and is_update:
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Invalid email address.")
        domain = email.split('@')[1]
        if domain not in self.ALLOWED_EMAIL_DOMAINS:
            raise ValidationError("Email domain is not allowed.")

    def validate_password(self, password, is_update=False):
        """Ensure that the password meets the specified requirements to maintain a secure password."""
        if not password and not is_update:
            raise ValidationError("password is required.")
        if not password and is_update:
            return
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

    def validate_first_name(self, first_name):
        """Ensure that the first name only contains characters, and is within the specified length."""
        if not first_name:
            return
        if not first_name.isalpha():
            raise ValidationError("First name must contain only alphabetic characters.")
        if len(first_name) < 1 or len(first_name) > 30:
            raise ValidationError("First name must be between 1 and 30 characters long.")

    def validate_last_name(self, last_name):
        """Ensure that the last name only contains characters, and is within the specified length."""
        if not last_name:
            return
        if not last_name.isalpha():
            raise ValidationError("Last name must contain only alphabetic characters.")
        if len(last_name) < 1 or len(last_name) > 30:
            raise ValidationError("Last name must be between 1 and 30 characters long.")

    def validate_profile_picture(self, profile_picture):
        """Ensure that the uploaded file is an image, verify its size, dimensions and file type."""
        if not profile_picture:
            return
        # Check if file is an image and if the MIME type is allowed
        if not profile_picture.content_type.startswith('image/') or profile_picture.content_type not in self.ALLOWED_IMAGE_TYPES:
            raise ValidationError("Uploaded file is not a supported image type")

        # Check file size (limit to 2MB)
        if profile_picture.size > 2 * 1024 * 1024:
            raise ValidationError("Image file size should not exceed 2MB")

        # Check image dimensions (e.g., limit to 1024x1024 pixels)
        width, height = get_image_dimensions(profile_picture)
        if width > 1024 or height > 1024:
            raise ValidationError("Image dimensions should not exceed 1024x1024 pixels")
