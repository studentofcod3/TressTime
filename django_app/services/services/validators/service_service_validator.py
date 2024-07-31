import re

from datetime import datetime
from django.core.exceptions import ValidationError


class ServiceServiceValidator:
    """
    ServiceValidator class validates the business logic for the Service entity.

    Methods:
        validate_service_data(service_data, is_update=False)
        validate_created_at(created_at)
        validate_updated_at(updated_at)
        validate_name(name)
        validate_description(description)
        validate_price(price)
        validate_duration(duration)
        validate_category(category)
        validate_created_at(created_at)
        validate_updated_at(updated_at)
    """
    def validate_service_exists(self, service, service_id):
        if not service:
            raise ValidationError(f"Service with ID {service_id} does not exist.")
        
    def validate_service_data(self, service_data, is_update=False):
        """
        Validates service data.
        
        This contains any business logic validation (e.g., string length, value ranges, format checks).
        Any database level constraints (e.g., unique constraints, field types, nullability) should be defined on the model.
        """
        if is_update:
            if 'id' in service_data:
                raise ValidationError("ID cannot be modified.")
            self.validate_updated_at(service_data.get('updated_at', None))
        else:
            self.validate_created_at(service_data.get('created_at', None))
            self.validate_updated_at(service_data.get('updated_at', None))
        self.validate_name(service_data['name'])
        self.validate_description(service_data['description'])
        self.validate_duration(service_data['duration'])
        self.validate_price(service_data['price'])

    def validate_created_at(self, created_at):
        """
        Validates the created_at timestamp.

        Args:
            created_at (datetime): The created_at timestamp to validate.

        Raises:
            ValidationError: If the created_at timestamp is invalid.
        """
        if created_at is None:
            raise ValidationError("created_at is required.")
        if not isinstance(created_at, datetime):
            raise ValidationError("created_at must be a datetime object.")
        if created_at.tzinfo is None or created_at.tzinfo.utcoffset(created_at) is None:
            raise ValidationError("created_at must be an aware datetime object with timezone information.")
        
    def validate_updated_at(self, updated_at):
        """
        Validates the updated_at timestamp.

        Args:
            updated_at (datetime): The updated_at timestamp to validate.

        Raises:
            ValidationError: If the updated_at timestamp is invalid.
        """
        if updated_at is None:
            raise ValidationError("updated_at is required.")
        if not isinstance(updated_at, datetime):
            raise ValidationError("updated_at must be a datetime object.")
        if updated_at.tzinfo is None or updated_at.tzinfo.utcoffset(updated_at) is None:
            raise ValidationError("updated_at must be an aware datetime object with timezone information.")

    def validate_name(self, name):
        """Ensure the name exists and meets falls within the required length."""
        if not name:
            raise ValidationError("Service name is required.")
        min_allowed_length = 3
        max_allowed_length = 150
        if len(name) < min_allowed_length:
            raise ValidationError(f"Service name must be at least {min_allowed_length} characters long.")
        if len(name) > max_allowed_length:
            raise ValidationError(f"Service name must be no greater than {max_allowed_length} characters long.")
        
    def validate_description(self, description):
        """Ensure the description exists, meets falls within the required length."""
        if not description:
            raise ValidationError("Service description is required.")
        min_allowed_length = 10
        max_allowed_length = 2000
        if len(description) < min_allowed_length:
            raise ValidationError(f"Service description must be at least {min_allowed_length} characters long.")
        if len(description) > max_allowed_length:
            raise ValidationError(f"Service description must be no greater than {max_allowed_length} characters long.")
        
    def validate_duration(self, duration):
        """Ensure the duration exists and falls within the min/max times"""
        if not duration:
            raise ValidationError("Service duration is required.")
        min_allowed_duration = 10
        max_allowed_duration = 480
        if duration <= min_allowed_duration:
                raise ValidationError(f"Service duration must be at least {min_allowed_duration} minutes.")
        if duration > max_allowed_duration:
            raise ValidationError(f"Service duration must be no greater than {max_allowed_duration} minutes.")

    def validate_price(self, price):
        """Ensure the price exists, positive and has the required significant figures."""
        if not price:
            raise ValidationError("Service price is required.")
        if price <= 0:
            raise ValidationError("Service price must be a positive number.")
        if not re.match(r'^\d{1,3}(\.\d{1,2})?$', str(price)):
            raise ValidationError("Service price must have a maximum of 5 digits with up to 2 decimal places.")

        

