from abc import ABC, abstractmethod


class NotificationRepositoryInterface(ABC):
    @abstractmethod
    def get_notification_by_id(self, notification_id):
        pass

    @abstractmethod
    def get_all_notifications(self):
        pass

    @abstractmethod
    def create_notification(self, notification_data):
        pass

    @abstractmethod
    def update_notification(self, notification_id, notification_data):
        pass

    @abstractmethod
    def delete_notification(self, notification_id):
        pass 