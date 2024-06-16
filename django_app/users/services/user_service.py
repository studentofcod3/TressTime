from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware as make_aware_of_timezone

from users.services.validators.user_service_validator import UserServiceValidator
from users.repositories.user_repository import UserRepository
from users.services.interfaces.user_service_interface import UserServiceInterface


class UserService(UserServiceInterface):
    """
    UserService class handles the business logic for the User entity.

    Methods:
        get_user(user_id)
        get_all_users()
        create_user(user_data)
        update_user(user_id, user_data)
        delete_user(user_id)
    """

    def __init__(self):
        self.user_repository = UserRepository()
        self.validator = UserServiceValidator()

    def get_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        self.validator.validate_user_exists(user, user_id)
        return user
    
    def get_all_users(self):
        users = self.user_repository.get_all_users()
        return users

    def create_user(self, user_data):
        user_data['created_at'] = make_aware_of_timezone(datetime.now())
        user_data['updated_at'] = make_aware_of_timezone(datetime.now())
        if not self.validator.validate_user_data(user_data):
            raise ValidationError("Invalid user data provided.")
        try:
            self.user_repository.create_user(user_data)
        except Exception as e:
            raise ValidationError(f"Error creating user: {e}")

    def update_user(self, user_id, user_data):
        user = self.user_repository.get_user_by_id(user_id)
        self.validator.validate_user_exists(user, user_id)
        # Set updated_at timestamp and validate data before updating.
        user_data['updated_at'] = make_aware_of_timezone(datetime.now())
        self.validator.validate_user_data(user_data, is_update=True)
        try:
            return self.user_repository.update_user(user_id, user_data)
        except Exception as e:
            raise ValidationError(f"Error updating user: {e}")

    def delete_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        self.validator.validate_user_exists(user, user_id)
        try:
            return self.user_repository.delete_user(user_id)
        except Exception as e:
            raise ValidationError(f"Error deleting user: {e}")

