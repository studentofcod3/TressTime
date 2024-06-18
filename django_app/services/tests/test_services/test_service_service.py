import pytest

from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock

from services.services.service_service import ServiceService
from services.repositories.service_repository import ServiceRepository
from services.services.validators.service_service_validator import ServiceServiceValidator

class TestServiceService:
    """
    Test suite for the ServiceService class.

    This test suite ensures that the ServiceService class correctly implements business logic for service operations and
    uses the ServiceServiceValidator for validation.
    """

    @pytest.fixture
    def service_service(self):
        """
        Provides an instance of ServiceService with a mocked ServiceRepository and ServiceServiceValidator.
        """
        service = ServiceService()
        service.service_repository = MagicMock(spec=ServiceRepository)
        service.validator = MagicMock(spec=ServiceServiceValidator)
        return service

    def test_create_service_calls_validator(self, service_service):
        """
        Ensures that the create_service method calls the validator.
        """
        service_data = {'name': 'Haircut', 'description': 'A standard haircut', 'price': 25}
        service_service.validator.validate_service_data.return_value = None
        service_service.service_repository.create_service.return_value = service_data

        service_service.create_service(service_data)

        service_service.validator.validate_service_data.assert_called_once_with(service_data)
        service_service.service_repository.create_service.assert_called_once_with(service_data)

    def test_create_service_validation_error(self, service_service):
        """
        Ensures that the create_service method raises a ValidationError when validation fails.
        """
        service_data = {'name': '', 'description': 'A standard haircut', 'price': 25}
        service_service.validator.validate_service_data.side_effect = ValidationError("Service name is required")

        with pytest.raises(ValidationError, match="Service name is required"):
            service_service.create_service(service_data)

    def test_get_service(self, service_service):
        """
        Ensures that the get_service method retrieves a service by ID correctly.
        """
        service_id = 'some-unique-id'
        service_data = {'id': service_id, 'name': 'Haircut', 'description': 'A standard haircut', 'price': 25}
        service_service.service_repository.get_service_by_id.return_value = service_data

        service = service_service.get_service(service_id)

        service_service.service_repository.get_service_by_id.assert_called_once_with(service_id)
        assert service['id'] == service_id

    def test_update_service_calls_validator(self, service_service):
        """
        Ensures that the update_service method calls the validator.
        """
        service_id = 'some-unique-id'
        service_data = {'name': 'Updated Haircut', 'description': 'An updated haircut', 'price': 30}
        service_service.validator.validate_service_data.return_value = None
        service_service.service_repository.update_service.return_value = service_data

        service_service.update_service(service_id, service_data)

        service_service.validator.validate_service_data.assert_called_once_with(service_data, is_update=True)
        service_service.service_repository.update_service.assert_called_once_with(service_id, service_data)

    def test_update_service_validation_error(self, service_service):
        """
        Ensures that the update_service method raises a ValidationError when validation fails.
        """
        service_id = 'some-unique-id'
        service_data = {'name': '', 'description': 'An updated haircut', 'price': 30}
        service_service.validator.validate_service_data.side_effect = ValidationError("Service name is required")

        with pytest.raises(ValidationError, match="Service name is required"):
            service_service.update_service(service_id, service_data)

    def test_delete_service(self, service_service):
        """
        Ensures that the delete_service method deletes a service by ID correctly.
        """
        service_id = 'some-unique-id'
        service_service.service_repository.delete_service.return_value = True

        result = service_service.delete_service(service_id)

        service_service.service_repository.delete_service.assert_called_once_with(service_id)
        assert result is True

    def test_delete_service_not_found(self, service_service):
        """
        Ensures that the delete_service method handles the case where a service to be deleted is not found.
        """
        service_id = 'non-existent-id'
        service_service.service_repository.delete_service.return_value = False

        result = service_service.delete_service(service_id)

        service_service.service_repository.delete_service.assert_called_once_with(service_id)
        assert result is False