from unittest.mock import MagicMock, patch
import pytest

from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware as make_aware_of_timezone

from appointments.models import Appointment
from appointments.services.validators.appointment_service_validator import AppointmentServiceValidator


class TestAppointmentServiceValidator:
    """
    Test suite for the AppointmentServiceValidator class.

    This test suite ensures that the AppointmentServiceValidator class correctly validates appointment data,
    including starts_at, ends_at, status, confirmation_number created_at, and updated_at.
    
    Fixtures:
        - validator: Provides an instance of AppointmentServiceValidator for testing.
    """
    starts_at = make_aware_of_timezone(datetime.now())
    ends_at = make_aware_of_timezone(datetime.now() + timedelta(hours=1))

    @pytest.fixture
    def validator(self):
        """
        Provides an instance of AppointmentServiceValidator for testing.
        """
        return AppointmentServiceValidator()
    
    @pytest.fixture
    def mock_appointment(self):
        """A mock object for the Appointment model."""
        return MagicMock(spec=Appointment)
    
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
            appointment_data = {'id': 'some-id'}
            validator.validate_appointment_data(appointment_data, is_update=True)
    
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

    @pytest.mark.parametrize(
            'starts_at,ends_at',
            [
                (None, ends_at),
                (starts_at, None)
            ]
    )
    def test_validate_starts_at_ends_at_required(self, validator, starts_at, ends_at):
        """
        Ensures that an empty starts_at or ends_at raises a validation error.
        """
        with pytest.raises(ValidationError, match="Both starts_at and ends_at are required."):
            validator.validate_starts_at_ends_at(starts_at, ends_at)

    @pytest.mark.parametrize(
            'starts_at,ends_at',
            [
                ("2023-01-01", ends_at),
                (starts_at, "2023-01-01")
            ]
    )
    def test_validate_starts_at_ends_at_not_datetime(self, validator, starts_at, ends_at):
        with pytest.raises(ValidationError, match="Both starts_at and ends_at must be datetime objects."):
            validator.validate_starts_at_ends_at(starts_at, ends_at)
    
    @pytest.mark.parametrize(
            'starts_at,ends_at',
            [
                (datetime.now(), ends_at),
                (starts_at, datetime.now() + timedelta(hours=1) )
            ]
    )
    def test_validate_starts_at_ends_at_unaware(self, validator, starts_at, ends_at):
        with pytest.raises(ValidationError, match="Both starts_at and ends_at must be aware datetime objects with timezone information."):
            validator.validate_starts_at_ends_at(starts_at, ends_at)

    def test_validate_starts_at_after_ends_at(self, validator):
        with pytest.raises(ValidationError, match="End time cannot be earlier than end time."):
            validator.validate_starts_at_ends_at(self.ends_at, self.starts_at)

    def test_validate_status_required(self, validator):
        with pytest.raises(ValidationError, match="status is required."):
            validator.validate_status(None)

    @pytest.mark.parametrize(
            'status',
            [
                status for status in AppointmentServiceValidator.ALLOWED_APPOINTMENT_STATUSES
            ]
    )
    def test_validate_status_allowed(self, validator, status):
        validator.validate_status(status)

    def test_validate_status_not_allowed(self, validator):
        allowed_statuses_str = ", ".join(AppointmentServiceValidator.ALLOWED_APPOINTMENT_STATUSES)
        with pytest.raises(ValidationError, match=rf"status must be one of the following: {allowed_statuses_str}"):
            validator.validate_status('Fake status')

    def test_validate_confirmation_number_unique(self, mock_appointment, validator):
        confirmation_number = '123456789'
        mock_appointment.confirmation_number = confirmation_number
        mock_appointment.__str__.return_value = "Appointment"

        # Mock the queryset to return specific values
        mock_queryset = MagicMock()
        mock_queryset.values_list.return_value = [mock_appointment]

        with patch.object(Appointment.objects, 'filter', return_value=mock_queryset):
            validator.validate_confirmation_number(confirmation_number, mock_appointment.id)
        
        mock_appointment_duplicate = mock_appointment
        mock_queryset.values_list.return_value = [mock_appointment, mock_appointment_duplicate]
        
        duplicate_list_str = ", ".join([str(mock_appointment), str(mock_appointment_duplicate)])
        with patch.object(Appointment.objects, 'filter', return_value=mock_queryset):
            with pytest.raises(ValidationError, match=rf"[Multiple appointments ({duplicate_list_str}) with same confirmation number. Confirmation number must be unique]"):
                validator.validate_confirmation_number(confirmation_number, mock_appointment.id)

    @pytest.mark.parametrize(
            'confirmation_number',
            [
                '1234567891',
                '123'
            ]
    )
    def test_validate_confirmation_number_length(self, mock_appointment, validator, confirmation_number):
        mock_appointment.confirmation_number = confirmation_number

        # Mock the queryset to return specific values
        mock_queryset = MagicMock()
        mock_queryset.values_list.return_value = [mock_appointment]

        with patch.object(Appointment.objects, 'filter', return_value=mock_queryset):
            with pytest.raises(ValidationError, match="confirmation number must be 9 digits long"):
                validator.validate_confirmation_number(confirmation_number, mock_appointment.id)
