import pytest

from django.db import IntegrityError
from unittest.mock import patch, MagicMock

from users.repositories.user_repository import UserRepository
from users.models import CustomUser


class TestUserRepository:
    """
    Test suite for the UserRepository class.

    This test suite ensures that the UserRepository class adheres to its contract and correctly implements all CRUD
    (Create, Read, Update, Delete) operations for the User model. The tests verify the behavior of the repository
    methods using the unittest.mock library to mock Django's ORM interactions, allowing isolated and controlled testing.

    Fixtures:
        mock_user: Provides a mocked instance of the CustomUser model.
        user_repository: Provides an instance of the UserRepository class for testing.

    Tests:
        - test_get_user_by_id
        - test_get_user_by_id_not_found
        - test_get_all_users
        - test_create_user
        - test_create_user_invalid_data
        - test_update_user
        - test_update_user_with_invalid_data
        - test_update_user_not_found
        - test_delete_user
        - test_delete_user_not_found

    The tests utilize unittest.mock to patch Django ORM methods, allowing for the simulation of database interactions without
    requiring an actual database. This approach provides faster and more reliable tests by isolating the repository logic
    from the database layer.

    By running this test suite, we can ensure that the UserRepository class functions correctly and adheres to its expected
    behavior, maintaining the integrity and reliability of user data operations in the application.
    """

    @pytest.fixture
    def mock_user(self):
        """A mock object for the CustomUser model."""
        return MagicMock(spec=CustomUser)

    @pytest.fixture
    def user_repository(self):
        """An instance of UserRepository."""
        return UserRepository()
    
    def test_get_user_by_id(self, mock_user, user_repository):
        """Ensures that the get_user_by_id method retrieves a user by ID correctly."""
        user_id = 'some-unique-id'
        with patch.object(CustomUser.objects, 'get', return_value=mock_user) as mock_get:
            user = user_repository.get_user_by_id(user_id)
            mock_get.assert_called_once_with(id=user_id)
            assert user == mock_user

    def test_get_user_by_id_not_found(self, user_repository):
        """Ensures that the get_user_by_id method handles the case where a user is not found."""
        user_id = 'non-existent-id'
        with patch.object(CustomUser.objects, 'get', side_effect=CustomUser.DoesNotExist):
            user = user_repository.get_user_by_id(user_id)
            assert user is None
        
    def test_get_all_users(self, mock_user, user_repository):
        """Ensures that the get_all_users method retrieves all users correctly."""
        mock_users = [mock_user, mock_user]
        with patch.object(CustomUser.objects, 'all', return_value=mock_users) as mock_all:
            users = user_repository.get_all_users()
            mock_all.assert_called_once()
            assert users == mock_users

    def test_create_user(self, mock_user, user_repository):
        """Ensures that the create_user method handles user creation correctly."""
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        with patch.object(CustomUser.objects, 'create', return_value=mock_user) as mock_create:
            user = user_repository.create_user(user_data)
            mock_create.assert_called_once_with(**user_data)
            assert user == mock_user
    
    def test_create_user_invalid_data(self, user_repository):
        """Ensures that create_user handles IntegrityError correctly."""
        user_data = {
            'username': 'testuser',
            'email': None,  # This should trigger an IntegrityError due to not null constraint
            'password': 'testpassword'
        }
        with patch.object(CustomUser.objects, 'create', side_effect=IntegrityError) as mock_create:
            user = user_repository.create_user(user_data)
            mock_create.assert_called_once_with(**user_data)
            assert not user

    def test_update_user(self, mock_user, user_repository):
        """Ensures that the update_user method updates a user's details correctly."""
        user_id = 'some-unique-id'
        user_data = {
            'email': 'newemail@example.com'
        }
        assert mock_user.email != user_data["email"]
        with patch.object(CustomUser.objects, 'get', return_value=mock_user):
            updated_user = user_repository.update_user(user_id, user_data)
            for key, value in user_data.items():
                setattr(mock_user, key, value)
            mock_user.save.assert_called_once()
            assert updated_user == mock_user
            assert mock_user.email == user_data["email"]

    def test_update_user_with_invalid_data(self, user_repository):
        """Ensures that update_user handles IntegrityError correctly."""
        user_id = 'some-unique-id'
        invalid_user_data = {
            'email': 'invalid-email',  # Assume this is an invalid email format
        }
        with patch.object(CustomUser.objects, 'get', side_effect=IntegrityError):
            user = user_repository.update_user(user_id, invalid_user_data)
            assert not user

    def test_update_user_not_found(self, user_repository):
        """Ensures that the update_user method handles the case where a user to be updated is not found."""
        user_id = 'non-existent-id'
        user_data = {
            'email': 'newemail@example.com'
        }
        with patch.object(CustomUser.objects, 'get', side_effect=CustomUser.DoesNotExist):
            updated_user = user_repository.update_user(user_id, user_data)
            assert updated_user is None

    def test_delete_user(self, mock_user, user_repository):
        """Ensures that the delete_user method deletes a user by ID correctly."""
        user_id = 'some-unique-id'
        with patch.object(CustomUser.objects, 'get', return_value=mock_user):
            result = user_repository.delete_user(user_id)
            mock_user.delete.assert_called_once()
            assert result is True

    def test_delete_user_not_found(self, user_repository):
        """Ensures that the delete_user method handles the case where a user to be deleted is not found."""
        user_id = 'non-existent-id'
        with patch.object(CustomUser.objects, 'get', side_effect=CustomUser.DoesNotExist):
            result = user_repository.delete_user(user_id)
            assert result is False
