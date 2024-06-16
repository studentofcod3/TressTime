import pytest

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import MagicMock, patch

from users.services.validators.user_service_validator import UserServiceValidator
from users.repositories.user_repository import UserRepository
from users.services.user_service import UserService


class TestUserService:
    """
    Test suite for the UserService class.

    This test suite ensures that the UserService class correctly implements business logic and validation for user operations.
    The tests verify the behavior of the service methods using the unittest.mock library to mock repository interactions,
    allowing isolated and controlled testing.

    Fixtures:
        user_service: Provides an instance of the UserService class with a mocked UserRepository.

    Tests:
        - test_get_user
        - test_create_user_calls_validator
        - test_create_user_validation_error
        - test_update_user_calls_validator
        - test_update_user_validation_error
        - test_delete_user
        - test_delete_user_not_found
    """
    
    @pytest.fixture
    def user_service(self):
        """
        Provides an instance of UserService with a mocked UserRepository.
        """
        service = UserService()
        service.user_repository = MagicMock(spec=UserRepository)
        service.validator = MagicMock(spec=UserServiceValidator)
        return service

    def test_get_user(self, user_service):
        """
        Ensures that the get_user method retrieves a user by ID correctly.
        """
        user_id = 'some-unique-id'
        user_data = {'id': user_id, 'username': 'testuser'}
        user_service.user_repository.get_user_by_id.return_value = user_data

        user = user_service.get_user(user_id)
        
        user_service.user_repository.get_user_by_id.assert_called_once_with(user_id)
        assert user['id'] == user_id

    def test_create_user_calls_validator(self, user_service):
        """
        Ensures that the create_user method calls the validator.
        """
        user_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'Valid1Password!',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile_picture': SimpleUploadedFile('image.jpg', b'\x00' * 1024, content_type='image/jpeg')
        }

        with patch.object(UserRepository, 'create_user', return_value=user_data):
            user_service.create_user(user_data)
            user_service.validator.validate_user_data.assert_called_once_with(user_data)

    def test_create_user_validation_error(self, user_service):
        """
        Ensures that the create_user method raises a ValidationError when validation fails.
        """
        user_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'short',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile_picture': SimpleUploadedFile('image.jpg', b'\x00' * 1024, content_type='image/jpeg')
        }
        user_service.validator.validate_user_data.side_effect = ValidationError("Password must be at least 8 characters long.")
        with pytest.raises(ValidationError, match="Password must be at least 8 characters long."):
            user_service.create_user(user_data)

    def test_update_user_calls_validator(self, user_service):
        """
        Ensures that the update_user method calls the validator.
        """
        user_id = 'some-unique-id'
        user_data = {
            'email': 'newemail@gmail.com',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        with patch.object(UserRepository, 'update_user', return_value=user_data):
            user_service.update_user(user_id, user_data)
            user_service.validator.validate_user_data.assert_called_once_with(user_data, is_update=True)

    def test_update_user_validation_error(self, user_service):
        """
        Ensures that the update_user method raises a ValidationError when validation fails.
        """
        user_id = 'some-unique-id'
        user_data = {
            'email': 'invalidemail',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        user_service.validator.validate_user_data.side_effect = ValidationError("Invalid email address.")
        with pytest.raises(ValidationError, match="Invalid email address."):
            user_service.update_user(user_id, user_data)

    def test_delete_user(self, user_service):
        """
        Ensures that the delete_user method deletes a user by ID correctly.
        """
        user_id = 'some-unique-id'
        user_service.user_repository.delete_user.return_value = True
        
        result = user_service.delete_user(user_id)
        
        user_service.user_repository.delete_user.assert_called_once_with(user_id)
        assert result is True

    def test_delete_user_not_found(self, user_service):
        """
        Ensures that the delete_user method handles the case where a user to be deleted is not found.
        """
        user_id = 'non-existent-id'
        user_service.user_repository.delete_user.return_value = False
        
        result = user_service.delete_user(user_id)
        
        user_service.user_repository.delete_user.assert_called_once_with(user_id)
        assert result is False
