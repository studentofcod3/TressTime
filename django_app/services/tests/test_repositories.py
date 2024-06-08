
import pytest

from django.db import IntegrityError
from unittest.mock import MagicMock, patch

from services.models import Service
from services.repositories.service_repository import ServiceRepository


class TestServiceRepository:
    """
    Test suite for the ServiceRepository class.

    This test suite ensures that the ServiceRepository class adheres to its contract and correctly implements all CRUD
    (Create, Read, Update, Delete) operations for the Service model. The tests verify the behavior of the repository
    methods using the unittest.mock library to mock Django's ORM interactions, allowing isolated and controlled testing.

    Fixtures:
        mock_service: Provides a mocked instance of the Service model.
        service_repository: Provides an instance of the ServiceRepository class for testing.

    Tests:
        - test_get_service_by_id
        - test_get_service_by_id_not_found
        - test_get_all_services
        - test_create_service
        - test_create_service_invalid_data
        - test_update_service
        - test_update_service_with_invalid_data
        - test_update_service_not_found
        - test_delete_service
        - test_delete_service_not_found

    The tests utilize unittest.mock to patch Django ORM methods, allowing for the simulation of database interactions without
    requiring an actual database. This approach provides faster and more reliable tests by isolating the repository logic
    from the database layer.

    By running this test suite, we can ensure that the ServiceRepository class functions correctly and adheres to its expected
    behavior, maintaining the integrity and reliability of service data operations in the application.
    """
    @pytest.fixture
    def mock_service(self):
        """A mock object for the Service model."""
        return MagicMock(spec=Service)
    
    @pytest.fixture
    def service_repository(self):
        """An instance of ServiceRepository."""
        return ServiceRepository()
    
    def test_get_service_by_id(self, mock_service, service_repository):
        """Ensures that the get_service_by_id method retrieves a service by ID correctly."""
        service_id = 'some-unique-id'
        with patch.object(Service.objects, 'get', return_value=mock_service) as mock_get:
            service = service_repository.get_service_by_id(service_id)
            mock_get.assert_called_once_with(id=service_id)
            assert service == mock_service

    def test_get_service_by_id_not_found(self, service_repository):
        """Ensures that the get_service_by_id method handles the case where a service is not found."""
        service_id = 'some-unique-id'
        with patch.object(Service.objects, 'get', side_effect=Service.DoesNotExist):
            service = service_repository.get_service_by_id(service_id)
            assert service is None

    def test_get_all_services(self, mock_service, service_repository):
        """Ensures that the get_all_services method retrieves all services correctly."""
        mock_services = [mock_service, mock_service]
        with patch.object(Service.objects, 'all', return_value=mock_services) as mock_all:
            services = service_repository.get_all_services()
            mock_all.assert_called_once()
            assert services == mock_services

    def test_create_service(self, mock_service, service_repository):
        """Ensures that the create_service method handles service creation correctly."""
        service_data = {
            'name': 'test name',
            'description': 'test description',
            'duration': 30,
            'price': 40.5
        }
        with patch.object(Service.objects, 'create', return_value=mock_service) as mock_create:
            service = service_repository.create_service(service_data)
            mock_create.assert_called_once_with(**service_data)
            assert service == mock_service

    def test_create_service_invalid_data(self, service_repository):
         """Ensures that create_service handles IntegrityError correctly."""
         service_data = {
            'name': 'test name',
            'description': 'test description',
            'duration': None, # This should trigger an IntegrityError due to not null constraint
            'price': 40.5
         }
         with patch.object(Service.objects, 'create', side_effect=IntegrityError) as mock_create:
             service = service_repository.create_service(service_data)
             mock_create.assert_called_once_with(**service_data)
             assert not service

    def test_update_service(self, mock_service, service_repository):
        """Ensures that the update_service method updates a service's details correctly."""
        service_id = 'some-unique-id'
        service_data = {
            'description': 'new description'
        }
        assert mock_service.description != service_data["description"]
        with patch.object(Service.objects, 'get', return_value=mock_service):
            updated_service = service_repository.update_service(service_id, service_data)
            for key, value in service_data.items():
                setattr(mock_service, key, value)
            mock_service.save.assert_called_once()
            assert updated_service == mock_service
            assert updated_service.description == service_data["description"]


    def test_update_service_with_invalid_data(self, service_repository):
        """Ensures that update_service handles IntegrityError correctly."""
        service_id = 'some-unique-id'
        invalid_service_data = {
            'price': 'invalid-price',  # Assume this is an invalid price format
        }
        with patch.object(Service.objects, 'get', side_effect=IntegrityError):
            service = service_repository.update_service(service_id, invalid_service_data)
            assert not service


    def test_update_service_not_found(self, service_repository):
        """Ensures that the update_service method handles the case where a service to be updated is not found."""
        service_id = 'non-existent-id'
        service_data = {
            'email': 'newemail@example.com'
        }
        with patch.object(Service.objects, 'get', side_effect=Service.DoesNotExist):
            updated_service = service_repository.update_service(service_id, service_data)
            assert updated_service is None

    def test_delete_service(self, mock_service, service_repository):
        """Ensures that the delete_service method deletes a service by ID correctly."""
        service_id = 'some-unique-id'
        with patch.object(Service.objects, 'get', return_value=mock_service):
            result = service_repository.delete_service(service_id)
            mock_service.delete.assert_called_once()
            assert result is True

    def test_delete_service_not_found(self, service_repository):
        """Ensures that the delete_service method handles the case where a service to be deleted is not found."""
        service_id = 'non-existent-id'
        with patch.object(Service.objects, 'get', side_effect=Service.DoesNotExist):
            result = service_repository.delete_service(service_id)
            assert result is False
