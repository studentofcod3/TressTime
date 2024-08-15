from datetime import datetime
from django.urls import reverse
from django.utils.timezone import make_aware as make_aware_of_timezone
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from users.repositories.user_repository import UserRepository
from users.models import CustomUser
from users.services.user_service import UserService

class UserAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            created_at=make_aware_of_timezone(datetime.now()),
            updated_at=make_aware_of_timezone(datetime.now()),
            username='testuser', 
            email='testuser@gmail.com', 
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)
        self.user_service = UserService()
        self.user_repository = UserRepository()

    def test_create_user(self):
        url = reverse('customuser-list')
        data = {
            'username': 'testuser-1',
            'email': 'testuser-1@gmail.com',
            'password': 'Testpassword@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(username=data['username']).email, data['email'])

    def test_list_users(self):
        url = reverse('customuser-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CustomUser.objects.count())

    def test_retrieve_user(self):
        url = reverse('customuser-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        url = reverse('customuser-detail', kwargs={'pk': self.user.id})
        data = {
            'username': 'updateduser',
            'email': 'updateduser@gmail.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@gmail.com')
    
    def test_partial_update_user(self):
        url = reverse('customuser-detail', kwargs={'pk': self.user.id})
        data = {
            'first_name': 'PartiallyUpdated'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'PartiallyUpdated')

    def test_delete_user(self):
        url = reverse('customuser-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())
