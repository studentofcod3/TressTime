from abc import ABC, abstractmethod


class UserServiceInterface(ABC):
    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def create_user(self, user_data):
        pass

    @abstractmethod
    def update_user(self, user_id, user_data):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass
