from django.contrib.auth import get_user_model
from django.db import IntegrityError

from users.models import CustomUser
from .interfaces.user_repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def get_user_by_id(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except:
            return None
    
    def get_all_users(self):
        return CustomUser.objects.all()
    
    def create_user(self, user_data):
        try:
            return CustomUser.objects.create(**user_data)
        except IntegrityError:
            return None

    
    def update_user(self, user_id, user_data, partial=False):
        try:
            user = CustomUser.objects.get(id=user_id)
            for key, value in user_data.items():
                if partial and value is None:
                    continue
                setattr(user, key, value)
            user.save()
            return user
        except CustomUser.DoesNotExist:
            return None
        except IntegrityError:
            return None
    
    def delete_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False