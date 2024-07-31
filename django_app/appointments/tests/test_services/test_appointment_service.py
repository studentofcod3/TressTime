import pytest

from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware as make_aware_of_timezone
from unittest.mock import MagicMock

from appointments.services.appointment_service import AppointmentService
from appointments.repositories.appointment_repository import AppointmentRepository
from appointments.services.validators.appointment_service_validator import AppointmentServiceValidator


class TestAppointmentService:
    """
    Test suite for the AppointmentService class.

    This test suite ensures that the AppointmentService class correctly implements business logic for appointment operations and
    uses the AppointmentServiceValidator for validation.
    """
    
    @pytest.fixture
    def appointment_service(self):
        """
        Provides an instance of AppointmentService with a mocked AppointmentRepository and AppointmentServiceValidator.
        """
        service = AppointmentService()
        service.appointment_repository = MagicMock(spec=AppointmentRepository)
        service.validator = MagicMock(spec=AppointmentServiceValidator)
        return service

    def test_create_appointment_calls_validator(self, appointment_service):
        """
        Ensures that the create_appointment method calls the validator.
        """
        appointment_data = {
            'starts_at': 'some date',
            'ends_at': 'some other date',
            'status': 'scheduled',
        }
        appointment_service.validator.validate_appointment_data.return_value = None
        appointment_service.appointment_repository.create_appointment.return_value = appointment_data

        appointment_service.create_appointment(appointment_data)

        appointment_service.validator.validate_appointment_data.assert_called_once_with(appointment_data)
        appointment_service.appointment_repository.create_appointment.assert_called_once_with(appointment_data)

    def test_create_appointment_validation_error(self, appointment_service):
        """
        Ensures that the create_appointment method raises a ValidationError when validation fails.
        """
        appointment_data = {
            'starts_at': 'some date',
            'ends_at': 'some other date',
            'status': 'scheduled',
        }
        appointment_service.validator.validate_appointment_data.side_effect = ValidationError("Both starts_at and ends_at are required.")

        with pytest.raises(ValidationError, match="Both starts_at and ends_at are required."):
            appointment_service.create_appointment(appointment_data)

    def test_get_appointment(self, appointment_service):
        """
        Ensures that the get_appointment method retrieves an appointment by ID correctly.
        """
        appointment_id = 'some-unique-id'
        appointment_data = {
            'id': appointment_id,
            'starts_at': 'some date',
            'ends_at': 'some other date',
            'status': 'scheduled',
        }
        appointment_service.appointment_repository.get_appointment_by_id.return_value = appointment_data

        appointment = appointment_service.get_appointment(appointment_id)

        appointment_service.appointment_repository.get_appointment_by_id.assert_called_once_with(appointment_id)
        assert appointment['id'] == appointment_id

    def test_update_appointment_calls_validator(self, appointment_service):
        """
        Ensures that the update_appointment method calls the validator.
        """
        appointment_id = 'some-unique-id'
        appointment_data = {
            'id': appointment_id,
            'starts_at': 'some date',
            'ends_at': 'some other date',
            'status': 'scheduled',
        }
        appointment_service.validator.validate_appointment_data.return_value = None
        appointment_service.appointment_repository.update_appointment.return_value = appointment_data

        appointment_service.update_appointment(appointment_id, appointment_data)

        appointment_service.validator.validate_appointment_data.assert_called_once_with(appointment_data, is_update=True)
        appointment_service.appointment_repository.update_appointment.assert_called_once_with(appointment_id, appointment_data)

    def test_update_appointment_validation_error(self, appointment_service):
        """
        Ensures that the update_appointment method raises a ValidationError when validation fails.
        """
        appointment_id = 'some-unique-id'
        appointment_data = {'name': '', 'description': 'An updated haircut', 'price': 30}
        appointment_service.validator.validate_appointment_data.side_effect = ValidationError("End time cannot be earlier than end time")

        with pytest.raises(ValidationError, match="End time cannot be earlier than end time"):
            appointment_service.update_appointment(appointment_id, appointment_data)

    def test_delete_appointment(self, appointment_service):
        """
        Ensures that the delete_appointment method deletes an appointment by ID correctly.
        """
        appointment_id = 'some-unique-id'
        appointment_service.appointment_repository.delete_appointment.return_value = True

        result = appointment_service.delete_appointment(appointment_id)

        appointment_service.appointment_repository.delete_appointment.assert_called_once_with(appointment_id)
        assert result is True

    def test_delete_appointment_not_found(self, appointment_service):
        """
        Ensures that the delete_appointment method handles the case where an appointment to be deleted is not found.
        """
        appointment_id = 'non-existent-id'
        appointment_service.appointment_repository.delete_appointment.return_value = False

        result = appointment_service.delete_appointment(appointment_id)

        appointment_service.appointment_repository.delete_appointment.assert_called_once_with(appointment_id)
        assert result is False
