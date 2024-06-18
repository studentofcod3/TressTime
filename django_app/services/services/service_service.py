from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware as make_aware_of_timezone

from services.repositories.service_repository import ServiceRepository
from services.services.interfaces.service_service_interface import ServiceServiceInterface
from services.services.validators.service_service_validator import ServiceServiceValidator


class ServiceService(ServiceServiceInterface):
    """
    ServiceService class handles the business logic for the Service entity.

    Methods:
        get_service(service_id)
        get_all_services()
        create_service(service_data)
        update_service(service_id, service_data)
        delete_service(service_id)
    """

    def __init__(self):
        self.service_repository = ServiceRepository()
        self.validator = ServiceServiceValidator()

    def get_service(self, service_id):
        """Retrieves a service by its ID."""
        service = self.service_repository.get_service_by_id(service_id)
        self.validator.validate_service_exists(service, service_id)
        return service
    
    def get_all_services(self):
        """Retrieves all services."""
        services = self.service_repository.get_all_services()
        return services
    
    def create_service(self, service_data):
        """Validates and creates a new service."""
        service_data['created_at'] = make_aware_of_timezone(datetime.now())
        service_data['updated_at'] = make_aware_of_timezone(datetime.now())
        self.validator.validate_service_data(service_data)
        try:
            return self.service_repository.create_service(service_data)
        except Exception as e:
            raise ValidationError(f"Error creating service: {e}")
    
    def update_service(self, service_id, service_data):
        """Validates and updates an existing service."""
        # Ensure service instance exists
        service = self.service_repository.get_service_by_id(service_id)
        self.validator.validate_service_exists(service, service_id)
        # Set updated_at timestamp and validate data before updating.
        service_data['updated_at'] = make_aware_of_timezone(datetime.now())
        self.validator.validate_service_data(service_data, is_update=True)
        try:
            return self.service_repository.update_service(service_id, service_data)
        except Exception as e:
            raise ValidationError(f"Error updating service: {e}")
    
    def delete_service(self, service_id):
        """Deletes a service by its ID."""
        service = self.service_repository.get_service_by_id(service_id)
        self.validator.validate_service_exists(service, service_id)
        return self.service_repository.delete_service(service_id)
