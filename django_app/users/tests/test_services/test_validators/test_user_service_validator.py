import pytest

from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from users.services.validators.user_service_validator import UserServiceValidator

class TestUserServiceValidator:
    """
    Test suite for the UserServiceValidator class.

    This test suite ensures that the UserServiceValidator class correctly validates user data, including usernames,
    emails, passwords, first names, last names, and profile pictures.

    Fixtures:
        - validator: Provides an instance of UserServiceValidator for testing.
    """

    @pytest.fixture
    def validator(self):
        """
        Provides an instance of UserServiceValidator for testing.
        """
        return UserServiceValidator()
    
    def test_created_at_required(self, validator):
        """
        Ensures that a missing created_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="created_at is required."):
            validator.validate_created_at(None)

    def test_validate_created_at_invalid_type(self, validator):
        """
        Ensures that an invalid created_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="created_at must be a datetime object."):
            validator.validate_created_at("2023-01-01")

    def test_validate_created_at_naive_datetime(self, validator):
        """
        Ensures that a created_at timestamp without a timezone raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="created_at must be an aware datetime object with timezone information."):
            validator.validate_created_at(datetime.now())

    def test_validate_id_update(self, validator):
        """
        Ensures that an attempted update to the ID raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="ID cannot be modified."):
            user_data = {'id': 'some-id'}
            validator.validate_user_data(user_data, is_update=True)

    def test_validate_updated_at_required(self, validator):
        """
        Ensures that a missing updated_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="updated_at is required."):
            validator.validate_updated_at(None)

    def test_validate_updated_at_invalid_type(self, validator):
        """
        Ensures that an invalid updated_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="updated_at must be a datetime object."):
            validator.validate_updated_at("2023-01-01")

    def test_validate_updated_at_naive_datetime(self, validator):
        """
        Ensures that an updated_at timestamp without a timezone raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="updated_at must be an aware datetime object with timezone information."):
            validator.validate_updated_at(datetime.now())

    def test_validate_username_too_short(self, validator):
        """
        Ensures that a username shorter than 5 characters raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Username must be at least 5 characters long."):
            validator.validate_username("user")

    def test_validate_username_valid(self, validator):
        """
        Ensures that a valid username passes validation.
        """
        try:
            validator.validate_username("validuser")
        except ValidationError:
            pytest.fail("Unexpected ValidationError")

    def test_validate_email_required(self, validator):
        """Ensures that email is present."""
        with pytest.raises(ValidationError, match="email is required."):
            validator.validate_email(None)

    def test_validate_email_invalid(self, validator):
        """
        Ensures that an invalid email raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Invalid email address."):
            validator.validate_email("invalidemail")

    def test_validate_email_invalid_domain(self, validator):
        """
        Ensures that an email with a non-whitelisted domain raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Email domain is not allowed."):
            validator.validate_email("user@invalid.com")

    def test_validate_email_valid(self, validator):
        """
        Ensures that a valid email passes validation.
        """
        try:
            validator.validate_email("user@gmail.com")
        except ValidationError:
            pytest.fail("Unexpected ValidationError")

    def test_validate_password_too_short(self, validator):
        """
        Ensures that a password shorter than 8 characters raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Password must be at least 8 characters long."):
            validator.validate_password("Short1!")

    def test_validate_password_missing_uppercase(self, validator):
        """
        Ensures that a password without an uppercase letter raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Password must contain at least one uppercase letter."):
            validator.validate_password("lowercase1!")

    def test_validate_password_valid(self, validator):
        """
        Ensures that a valid password passes validation.
        """
        try:
            validator.validate_password("Valid1Password!")
        except ValidationError:
            pytest.fail("Unexpected ValidationError")

    def test_validate_first_name_invalid(self, validator):
        """
        Ensures that a first name with non-alphabetic characters raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="First name must contain only alphabetic characters."):
            validator.validate_first_name("John1")

    def test_validate_first_name_valid(self, validator):
        """
        Ensures that a valid first name passes validation.
        """
        try:
            validator.validate_first_name("John")
        except ValidationError:
            pytest.fail("Unexpected ValidationError")

    def test_validate_last_name_invalid(self, validator):
        """
        Ensures that a last name with non-alphabetic characters raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Last name must contain only alphabetic characters."):
            validator.validate_last_name("Doe1")

    def test_validate_last_name_valid(self, validator):
        """
        Ensures that a valid last name passes validation.
        """
        try:
            validator.validate_last_name("Doe")
        except ValidationError:
            pytest.fail("Unexpected ValidationError")

    def test_validate_profile_picture_invalid_type(self, validator):
        """
        Ensures that an unsupported profile picture file type raises a ValidationError.
        """
        invalid_image = SimpleUploadedFile('file.bmp', b'\x00' * 1024, content_type='image/bmp')
        with pytest.raises(ValidationError, match="Uploaded file is not a supported image type"):
            validator.validate_profile_picture(invalid_image)

    def test_validate_profile_picture_large_file(self, validator):
        """
        Ensures that a large profile picture raises a ValidationError.
        """
        large_image = SimpleUploadedFile('image.jpg', b'\x00' * (2 * 1024 * 1024 + 1), content_type='image/jpeg')
        with pytest.raises(ValidationError, match="Image file size should not exceed 2MB"):
            validator.validate_profile_picture(large_image)

    @patch('users.services.validators.user_service_validator.get_image_dimensions')
    def test_validate_profile_picture_large_dimensions(self, mock_get_image_dimensions, validator):
        """
        Ensures that an oversized profile picture raises a ValidationError.
        """
        large_image = SimpleUploadedFile('large_image.jpg', b'\x00' * 1024, content_type='image/jpeg')
        mock_get_image_dimensions.return_value = (2048, 2048)
        with pytest.raises(ValidationError, match="Image dimensions should not exceed 1024x1024 pixels"):
            validator.validate_profile_picture(large_image)

    @patch('users.services.validators.user_service_validator.get_image_dimensions')
    def test_validate_profile_picture_valid(self, mock_get_image_dimensions, validator):
        """
        Ensures that a valid profile picture passes validation.
        """
        valid_image = SimpleUploadedFile('image.jpg', b'\x00' * 1024, content_type='image/jpeg')
        mock_get_image_dimensions.return_value = (800, 800)
        with patch('django.core.files.images.get_image_dimensions', return_value=(800, 800)):
            try:
                validator.validate_profile_picture(valid_image)
            except ValidationError:
                pytest.fail("Unexpected ValidationError")