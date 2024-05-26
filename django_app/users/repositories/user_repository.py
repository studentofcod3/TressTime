from django.contrib.auth import get_user_model

from users.models import CustomUser
from .interfaces.user_repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    # TODO: Test for exceptions
    def get_user_by_id(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except:
            return None
    
    def get_all_users(self):
        return CustomUser.objects.all()
    
    def create_user(self, user_data):
        # TODO: Add try catch in case missing data and test for this
        return CustomUser.objects.create(**user_data)
    
    def update_user(self, user_id, user_data):
        try:
            user = CustomUser.objects.get(id=user_id)
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()
            return user
        except CustomUser.DoesNotExist:
            return None
        except:
            # TODO: Find error for when updates with non-existent field
            return None
    
    def delete_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False