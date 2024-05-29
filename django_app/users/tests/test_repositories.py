import pytest

from django.db import IntegrityError
from unittest.mock import patch, MagicMock

from users.repositories.user_repository import UserRepository
from users.models import CustomUser


class TestUserRepository:

    @pytest.fixture
    def mock_user(self):
        """A mock object for the CustomUser model."""
        return MagicMock(spec=CustomUser)

    @pytest.fixture
    def user_repository(self):
        """An instance of UserRepository."""
        return UserRepository()
    
    def test_get_user_by_id(self, mock_user, user_repository):
        """Ensures get_user_by_id calls User.objects.get with the correct parameters and returns the mock user."""
        user_id = 'some-unique-id'
        with patch.object(CustomUser.objects, 'get', return_value=mock_user) as mock_get:
            user = user_repository.get_user_by_id(user_id)
            mock_get.assert_called_once_with(id=user_id)
            assert user == mock_user

    def test_get_user_by_id_not_found(self, user_repository):
        """Ensures get_user_by_id handles User.DoesNotExist correctly."""
        user_id = 'non-existent-id'
        with patch.object(CustomUser.objects, 'get', side_effect=CustomUser.DoesNotExist):
            user = user_repository.get_user_by_id(user_id)
            assert user is None
        
    def test_get_all_users(self, mock_user, user_repository):
        """Checks that get_all_users calls the 'all' method exactly once and returns the expected list of users."""
        mock_users = [mock_user, mock_user]
        with patch.object(CustomUser.objects, 'all', return_value=mock_users) as mock_all:
            users = user_repository.get_all_users()
            mock_all.assert_called_once()
            assert users == mock_users

    def test_create_user(self, mock_user, user_repository):
        """Ensures create_user calls User.objects.create with the correct parameters and returns the mock user."""
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
        """Ensures update_user updates the user and saves it."""
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
        """Ensures update_user handles User.DoesNotExist correctly."""
        user_id = 'non-existent-id'
        user_data = {
            'email': 'newemail@example.com'
        }
        with patch.object(CustomUser.objects, 'get', side_effect=CustomUser.DoesNotExist):
            updated_user = user_repository.update_user(user_id, user_data)
            assert updated_user is None

    def test_delete_user(self, mock_user, user_repository):
        """Ensures delete_user deletes the user and returns True."""
        user_id = 'some-unique-id'
        with patch.object(CustomUser.objects, 'get', return_value=mock_user):
            result = user_repository.delete_user(user_id)
            mock_user.delete.assert_called_once()
            assert result is True

    def test_delete_user_not_found(self, user_repository):
        """Ensures delete_user handles User.DoesNotExist correctly and returns False."""
        user_id = 'non-existent-id'
        with patch.object(CustomUser.objects, 'get', side_effect=CustomUser.DoesNotExist):
            result = user_repository.delete_user(user_id)
            assert result is False
