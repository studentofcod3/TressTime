import pytest

from django.db import IntegrityError
from unittest.mock import MagicMock, patch

from notifications.models import Notification
from notifications.repositories.notification_repository import NotificationRepository

class TestNotificationRepository:
    """
    Test suite for the NotificationRepository class.

    This test suite ensures that the NotificationRepository class adheres to its contract and correctly implements all CRUD
    (Create, Read, Update, Delete) operations for the Notification model. The tests verify the behavior of the repository
    methods using the unittest.mock library to mock Django's ORM interactions, allowing isolated and controlled testing.

    Fixtures:
        mock_notification: Provides a mocked instance of the Notification model.
        notification_repository: Provides an instance of the NotificationRepository class for testing.

    Tests:
        - test_get_notification_by_id
        - test_get_notification_by_id_not_found
        - test_get_all_notifications
        - test_create_notification
        - test_create_notification_invalid_data
        - test_update_notification
        - test_update_notification_with_invalid_data
        - test_update_notification_not_found
        - test_delete_notification
        - test_delete_notification_not_found

    The tests utilize unittest.mock to patch Django ORM methods, allowing for the simulation of database interactions without
    requiring an actual database. This approach provides faster and more reliable tests by isolating the repository logic
    from the database layer.

    By running this test suite, we can ensure that the NotificationRepository class functions correctly and adheres to its expected
    behavior, maintaining the integrity and reliability of notification data operations in the application.
    """

    @pytest.fixture
    def mock_notification(self):
        """A mock object for the Notification model."""
        return MagicMock(spec=Notification)
    
    @pytest.fixture
    def notification_repository(self):
        """An instance of NotificationRepository."""
        return NotificationRepository()
    
    def test_get_notification_by_id(self, mock_notification, notification_repository):
        """Ensures that the get_notification_by_id method retrieves a notification by ID correctly."""
        notification_id = 'some-unique-id'
        with patch.object(Notification.objects, 'get', return_value=mock_notification) as mock_get:
            notification = notification_repository.get_notification_by_id(notification_id)
            mock_get.assert_called_once_with(id=notification_id)
            assert notification == mock_notification

    def test_get_notification_by_id_not_found(self, notification_repository):
        """Ensures that the get_notification_by_id method handles the case where a notification is not found."""
        notification_id = 'some-unique-id'
        with patch.object(Notification.objects, 'get', side_effect=Notification.DoesNotExist):
            notification = notification_repository.get_notification_by_id(notification_id)
            assert notification is None

    def test_get_all_notifications(self, mock_notification, notification_repository):
        """Ensures that the get_all_notifications method retrieves all notifications correctly."""
        mock_notifications = [mock_notification, mock_notification]
        with patch.object(Notification.objects, 'all', return_value=mock_notifications) as mock_all:
            notifications = notification_repository.get_all_notifications()
            mock_all.assert_called_once()
            assert notifications == mock_notifications

    def test_create_notification(self, mock_notification, notification_repository):
        """Ensures that the create_notification method handles notification creation correctly."""
        notification_data = {
            'type': 'sms',
            'status': 'sent',
            'message': 'lorem ipsum',
            'scheduled_send_datetime': '12:34:45 05.06.2024',
            'priority': 'high',
            'user': 'The associated user'
        }
        with patch.object(Notification.objects, 'create', return_value=mock_notification) as mock_create:
            notification = notification_repository.create_notification(notification_data)
            mock_create.assert_called_once_with(**notification_data)
            assert notification == mock_notification

    def test_create_notification_invalid_data(self, notification_repository):
        """Ensures that create_notification handles IntegrityError correctly."""
        notification_data = {
            'type': 'sms',
            'status': 'pending',
            'message': 'lorem ipsum',
            'scheduled_send_datetime': '12:34:45 05.06.2024',
            'priority': None, # This should trigger an IntegrityError due to not null constraint
            'user': 'The associated user'
        }
        with patch.object(Notification.objects, 'create', side_effect=IntegrityError) as mock_create:
            notification = notification_repository.create_notification(notification_data)
            mock_create.assert_called_once_with(**notification_data)
            assert not notification

    def test_update_notification(self, mock_notification, notification_repository):
        """Ensures update_notification updates the notification and saves it."""
        notification_id = 'some-unique-id'
        notification_data = {
            'status': 'new status, ie: sent'
        }
        assert mock_notification.status != notification_data["status"]
        with patch.object(Notification.objects, 'get', return_value=mock_notification):
            updated_notification = notification_repository.update_notification(notification_id, notification_data)
            for key, value in notification_data.items():
                setattr(mock_notification, key, value)
            mock_notification.save.assert_called_once()
            assert updated_notification == mock_notification
            assert updated_notification.status == notification_data["status"]

    def test_update_notification_with_invalid_data(self, notification_repository):
        """Ensures that update_notification handles IntegrityError correctly."""
        notification_id = 'some-unique-id'
        invalid_notification_data = {
            'type': 'invalid-type',  # Assume this is an invalid type format
        }
        with patch.object(Notification.objects, 'get', side_effect=IntegrityError):
            notification = notification_repository.update_notification(notification_id, invalid_notification_data)
            assert not notification

    def test_update_notification_not_found(self, notification_repository):
        """Ensures that the update_notification method handles the case where a notification to be updated is not found."""
        notification_id = 'non-existent-id'
        notification_data = {
            'scheduled_send_datetime': '16:28:40 05.07.2024'
        }
        with patch.object(Notification.objects, 'get', side_effect=Notification.DoesNotExist):
            updated_notification = notification_repository.update_notification(notification_id, notification_data)
            assert updated_notification is None

    def test_delete_notification(self, mock_notification, notification_repository):
        """Ensures that the delete_notification method deletes a notification by ID correctly."""
        notification_id = 'some-unique-id'
        with patch.object(Notification.objects, 'get', return_value=mock_notification):
            result = notification_repository.delete_notification(notification_id)
            mock_notification.delete.assert_called_once()
            assert result is True

    def test_delete_notification_not_found(self, notification_repository):
        """Ensures that the delete_notification method handles the case where a notification to be deleted is not found."""
        notification_id = 'non-existent-id'
        with patch.object(Notification.objects, 'get', side_effect=Notification.DoesNotExist):
            result = notification_repository.delete_notification(notification_id)
            assert result is False
