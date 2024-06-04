import pytest

from django.db import IntegrityError
from unittest.mock import MagicMock, patch

from notifications.models import Notification
from notifications.repositories.notification_repository import NotificationRepository

class TestNotificationRepository:
    @pytest.fixture
    def mock_notification(self):
        """A mock object for the Notification model."""
        return MagicMock(spec=Notification)
    
    @pytest.fixture
    def notification_repository(self):
        """An instance of NotificationRepository."""
        return NotificationRepository()
    
    def test_get_notification_by_id(self, mock_notification, notification_repository):
        """Ensures get_notification_by_id calls Notification.objects.get with the correct parameters and returns the mock notification."""
        notification_id = 'some-unique-id'
        with patch.object(Notification.objects, 'get', return_value=mock_notification) as mock_get:
            notification = notification_repository.get_notification_by_id(notification_id)
            mock_get.assert_called_once_with(id=notification_id)
            assert notification == mock_notification

    def test_get_notification_by_id_not_found(self, notification_repository):
        """Ensures get_notification_by_id handles Notification.DoesNotExist correctly."""
        notification_id = 'some-unique-id'
        with patch.object(Notification.objects, 'get', side_effect=Notification.DoesNotExist):
            notification = notification_repository.get_notification_by_id(notification_id)
            assert notification is None

    def test_get_all_notifications(self, mock_notification, notification_repository):
        """Checks that get_all_notifications calls Notification.objects.all exactly once and returns the expected list of notifications."""
        mock_notifications = [mock_notification, mock_notification]
        with patch.object(Notification.objects, 'all', return_value=mock_notifications) as mock_all:
            notifications = notification_repository.get_all_notifications()
            mock_all.assert_called_once()
            assert notifications == mock_notifications

    def test_create_notification(self, mock_notification, notification_repository):
        """Ensures create_notification calls Notification.objects.create with the correct parameters and returns the notification."""
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
        """Ensures update_notification handles Notification.DoesNotExist correctly."""
        notification_id = 'non-existent-id'
        notification_data = {
            'scheduled_send_datetime': '16:28:40 05.07.2024'
        }
        with patch.object(Notification.objects, 'get', side_effect=Notification.DoesNotExist):
            updated_notification = notification_repository.update_notification(notification_id, notification_data)
            assert updated_notification is None

    def test_delete_notification(self, mock_notification, notification_repository):
        """Ensures delete_notification deletes the notification and returns True."""
        notification_id = 'some-unique-id'
        with patch.object(Notification.objects, 'get', return_value=mock_notification):
            result = notification_repository.delete_notification(notification_id)
            mock_notification.delete.assert_called_once()
            assert result is True

    def test_delete_notification_not_found(self, notification_repository):
        """Ensures delete_notification handles Notification.DoesNotExist correctly and returns False."""
        notification_id = 'non-existent-id'
        with patch.object(Notification.objects, 'get', side_effect=Notification.DoesNotExist):
            result = notification_repository.delete_notification(notification_id)
            assert result is False
