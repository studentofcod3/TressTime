import pytest

from datetime import datetime
from django.core.exceptions import ValidationError

from services.services.validators.service_service_validator import ServiceServiceValidator


class TestServiceServiceValidator:
    """
    Test suite for the ServiceServiceValidator class.

    This test suite ensures that the ServiceServiceValidator class correctly validates service data,
    including name, description, price, duration, category, created_at, and updated_at.
    
    Fixtures:
        - validator: Provides an instance of ServiceServiceValidator for testing.
    """

    @pytest.fixture
    def validator(self):
        """
        Provides an instance of ServiceServiceValidator for testing.
        """
        return ServiceServiceValidator()
    
    def test_created_at(self, validator):
        """
        Ensures that a missing created_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="created_at is required."):
            validator.validate_created_at(None)

    def test_validate_created_at_invalid_type(self, validator):
        """
        Ensures that an invalid created_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="created_at must be a datetime object."):
            validator.validate_created_at("2023-01-01")

    def test_validate_created_at_naive_datetime(self, validator):
        """
        Ensures that a created_at timestamp without a timezone raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="created_at must be an aware datetime object with timezone information."):
            validator.validate_created_at(datetime.now())

    def test_validate_id_update(self, validator):
        """
        Ensures that an attempted update to the ID raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="ID cannot be modified."):
            service_data = {'id': 'some-id'}
            validator.validate_service_data(service_data, is_update=True)
    
    def test_validate_updated_at_required(self, validator):
        """
        Ensures that a missing updated_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="updated_at is required."):
            validator.validate_updated_at(None)

    def test_validate_updated_at_invalid_type(self, validator):
        """
        Ensures that an invalid updated_at timestamp raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="updated_at must be a datetime object."):
            validator.validate_updated_at("2023-01-01")

    def test_validate_updated_at_naive_datetime(self, validator):
        """
        Ensures that an updated_at timestamp without a timezone raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="updated_at must be an aware datetime object with timezone information."):
            validator.validate_updated_at(datetime.now())

    def test_validate_name_required(self, validator):
        """
        Ensures that an empty service name raises a validation error.
        """
        with pytest.raises(ValidationError, match='Service name is required.'):
            validator.validate_name(None)

    def test_validate_name_too_short(self, validator):
        """
        Ensures that a service name shorter the allowed length raises a validation error.
        """
        min_allowed_length = 3
        with pytest.raises(ValidationError, match=f'Service name must be at least {min_allowed_length} characters long.'):
            validator.validate_name('A' * (min_allowed_length - 1))

    def test_validate_name_too_long(self, validator):
        """
        Ensures that a service name longer than the allowed length raises a validation error.
        """
        max_allowed_length = 150
        with pytest.raises(ValidationError, match=f'Service name must be no greater than {max_allowed_length} characters'):
            validator.validate_name('A' * (max_allowed_length + 1))

    def test_validate_description_required(self, validator):
        """
        Ensures that an empty service description raises a validation error.
        """
        with pytest.raises(ValidationError, match='Service description is required.'):
            validator.validate_description(None)
    
    def test_validate_description_too_short(self, validator):
        """
        Ensures that a service description shorter than the allowed length raises a validation error.
        """
        min_allowed_length = 10
        with pytest.raises(ValidationError, match=f"Service description must be at least {min_allowed_length} characters long."):
            validator.validate_description('A' * (min_allowed_length - 1))
    
    def test_validate_description_too_long(self, validator):
        """
        Ensures that a service description longer than the allowed length raises a validation error.
        """
        max_allowed_length = 2000
        with pytest.raises(ValidationError, match=f"Service description must be no greater than {max_allowed_length} characters long."):
            validator.validate_description('A' * (max_allowed_length + 1))

    def test_validate_duration_required(self, validator):
        """
        Ensures that an empty service duration raises a validation error.
        """
        with pytest.raises(ValidationError, match='Service duration is required.'):
            validator.validate_duration(None)

    def test_validate_duration_too_short(self, validator):
        """
        Ensures that a service duration no greater than the allowed amount raises a ValidationError.
        """
        min_allowed_duration = 10
        with pytest.raises(ValidationError, match=f"Service duration must be at least {min_allowed_duration} minutes."):
            validator.validate_duration(min_allowed_duration - 1)

    def test_validate_duration_too_long(self, validator):
        """
        Ensures that a service duration longer than the allowed amount raises a ValidationError.
        """
        max_allowed_duration = 480
        with pytest.raises(ValidationError, match="Service duration must be no greater than 480 minutes."):
            validator.validate_duration(max_allowed_duration + 1)

    def test_validate_price_required(self, validator):
        """
        Ensures that a missing service price raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Service price is required."):
            validator.validate_price(None)

    def test_validate_price_positive(self, validator):
        """
        Ensures that a non-positive service price raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Service price must be a positive number."):
            validator.validate_price(-50)

    def test_validate_price_format(self, validator):
        """
        Ensures that a service price with invalid format raises a ValidationError.
        """
        with pytest.raises(ValidationError, match="Service price must have a maximum of 5 digits with up to 2 decimal places."):
            validator.validate_price(12345.678)

        with pytest.raises(ValidationError, match="Service price must have a maximum of 5 digits with up to 2 decimal places."):
            validator.validate_price(123456)

        with pytest.raises(ValidationError, match="Service price must have a maximum of 5 digits with up to 2 decimal places."):
            validator.validate_price(1234.567)

        # Valid formats
        try:
            validator.validate_price(123.45)
            validator.validate_price(12.34)
            validator.validate_price(123)
        except ValidationError:
            pytest.fail("Unexpected ValidationError for valid price format.")
