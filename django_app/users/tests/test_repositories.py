
import pytest
from users.repositories.user_repository import UserRepository
from users.models import CustomUser


@pytest.mark.django_db
class TestUserRepository:
    # TODO: Docstrings
    # TODO: Non happy paths

    user_repository = UserRepository()

    username='test_username'
    username_2='test_username_2'
    email='test_email'
    email_2='test_email_2'
    password='test_password'
    password_2='test_password_2'
    
    def create_user(self):
        return CustomUser.objects.create(
            username=self.username,
            email=self.email,
            password=self.password
        )
    
    def create_second_user(self):
        return CustomUser.objects.create(
            username=self.username_2,
            email=self.email_2,
            password=self.password_2
        )
    
    def test_get_user_id(self):
        custom_user = self.create_user()
        
        user = self.user_repository.get_user_by_id(custom_user.id)
        assert user.username == self.username
        assert user.email == self.email
        assert user.password == self.password
        

    def test_get_all_users(self):
        custom_user = self.create_user()
        custom_user_2 = self.create_second_user()

        all_users = self.user_repository.get_all_users()

        assert len(all_users) == 2
        assert custom_user in all_users
        assert custom_user_2 in all_users


    def test_create_user(self):
        new_user = self.user_repository.create_user(
            user_data={
                'username': self.username,
                'email': self.email,
                'password':self.password,
            }
        )
        assert new_user.username == self.username
        assert new_user.email == self.email
        assert new_user.password == self.password

    def test_update_user(self):
        custom_user = self.create_user()

        updated_user = self.user_repository.update_user(
            user_id=custom_user.id,
            user_data={
                'username': self.username_2,
            }
        )
        assert updated_user.id == custom_user.id
        assert updated_user.username == self.username_2
        # Other fields should remain the same
        assert updated_user.email == self.email
        assert updated_user.password == self.password

    def test_delete_user(self):
        custom_user = self.create_user()
        assert len(self.user_repository.get_all_users()) == 1
        
        self.user_repository.delete_user(
            user_id=custom_user.id
        )
        assert len(self.user_repository.get_all_users()) == 0
