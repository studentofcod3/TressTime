from django.db import IntegrityError
from notifications.models import Notification
from notifications.repositories.interfaces.notification_repository_interface import NotificationRepositoryInterface


class NotificationRepository(NotificationRepositoryInterface):
    def get_notification_by_id(self, notification_id):
        try:
            return Notification.objects.get(id=notification_id)
        except:
            return None
    
    def get_all_notifications(self):
        return Notification.objects.all()
    
    def create_notification(self, notification_data):
        try:
            return Notification.objects.create(**notification_data)
        except IntegrityError:
            return None
    
    def update_notification(self, notification_id, notification_data):
        try:
            notification = Notification.objects.get(id=notification_id)
            for key, value in notification_data.items():
                setattr(notification, key, value)
            notification.save()
            return notification
        except Notification.DoesNotExist:
            return None
        except IntegrityError:
            return None
    
    def delete_notification(self, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return True
        except Notification.DoesNotExist:
            return False