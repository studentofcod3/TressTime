import pytest

from django.db import IntegrityError
from unittest.mock import MagicMock, patch

from appointments.models import Appointment
from appointments.repositories.appointment_repository import AppointmentRepository


class TestAppointmentRepository:
    @pytest.fixture
    def mock_appointment(self):
        """A mock object for the Appointment model."""
        return MagicMock(spec=Appointment)
    
    @pytest.fixture
    def appointment_repository(self):
        """An instance of AppointmentRepository."""
        return AppointmentRepository()
    
    def test_get_appointment_by_id(self, mock_appointment, appointment_repository):
        """Ensures get_appointment_by_id calls Appointment.objects.get with the correct parameters and returns the mock appointment."""
        appointment_id = 'some-unique-id'
        with patch.object(Appointment.objects, 'get', return_value=mock_appointment) as mock_get:
            appointment = appointment_repository.get_appointment_by_id(appointment_id)
            mock_get.assert_called_once_with(id=appointment_id)
            assert appointment == mock_appointment

    def test_get_appointment_by_id_not_found(self, appointment_repository):
        """Ensures get_appointment_by_id handles Appointment.DoesNotExist correctly."""
        appointment_id = 'some-unique-id'
        with patch.object(Appointment.objects, 'get', side_effect=Appointment.DoesNotExist):
            appointment = appointment_repository.get_appointment_by_id(appointment_id)
            assert appointment is None

    def test_get_all_appointments(self, mock_appointment, appointment_repository):
        """Checks that get_all_appointments calls Appointment.objects.all exactly once and returns the expected list of appointments."""
        mock_appointments = [mock_appointment, mock_appointment]
        with patch.object(Appointment.objects, 'all', return_value=mock_appointments) as mock_all:
            appointments = appointment_repository.get_all_appointments()
            mock_all.assert_called_once()
            assert appointments == mock_appointments

    def test_create_appointment(self, mock_appointment, appointment_repository):
        """Ensures create_appointment calls Appointment.objects.create with the correct parameters and returns the appointment."""
        appointment_data = {
            'starts_at': 'The start time of the appointment',
            'ends_at': 'The end time of the appointment',
            'status': 'The current status of the appointment',
            'user': 'The associated user',
            'service': 'The associated service',
        }
        with patch.object(Appointment.objects, 'create', return_value=mock_appointment) as mock_create:
            appointment = appointment_repository.create_appointment(appointment_data)
            mock_create.assert_called_once_with(**appointment_data)
            assert appointment == mock_appointment

    def test_create_appointment_invalid_data(self, appointment_repository):
        """Ensures that create_appointment handles IntegrityError correctly."""
        appointment_data = {
            'starts_at': 'The start time of the appointment',
            'ends_at': 'The end time of the appointment',
            'status': 'The current status of the appointment',
            'user': None, # This should trigger an IntegrityError due to not null constraint
            'service': 'The associated service',
        }
        with patch.object(Appointment.objects, 'create', side_effect=IntegrityError) as mock_create:
            appointment = appointment_repository.create_appointment(appointment_data)
            mock_create.assert_called_once_with(**appointment_data)
            assert not appointment

    def test_update_appointment(self, mock_appointment, appointment_repository):
        """Ensures update_appointment updates the appointment and saves it."""
        appointment_id = 'some-unique-id'
        appointment_data = {
            'status': 'new status'
        }
        assert mock_appointment.status != appointment_data["status"]
        with patch.object(Appointment.objects, 'get', return_value=mock_appointment):
            updated_appointment = appointment_repository.update_appointment(appointment_id, appointment_data)
            for key, value in appointment_data.items():
                setattr(mock_appointment, key, value)
            mock_appointment.save.assert_called_once()
            assert updated_appointment == mock_appointment
            assert updated_appointment.status == appointment_data["status"]

    def test_update_appointment_with_invalid_data(self, appointment_repository):
        """Ensures that update_appointment handles IntegrityError correctly."""
        appointment_id = 'some-unique-id'
        invalid_appointment_data = {
            'status': 6,  # Assume this is an invalid status format
        }
        with patch.object(Appointment.objects, 'get', side_effect=IntegrityError):
            appointment = appointment_repository.update_appointment(appointment_id, invalid_appointment_data)
            assert not appointment

    def test_update_appointment_not_found(self, appointment_repository):
        """Ensures update_appointment handles Appointment.DoesNotExist correctly."""
        appointment_id = 'non-existent-id'
        appointment_data = {
            'email': 'newemail@example.com'
        }
        with patch.object(Appointment.objects, 'get', side_effect=Appointment.DoesNotExist):
            updated_appointment = appointment_repository.update_appointment(appointment_id, appointment_data)
            assert updated_appointment is None

    def test_delete_appointment(self, mock_appointment, appointment_repository):
        """Ensures delete_appointment deletes the appointment and returns True."""
        appointment_id = 'some-unique-id'
        with patch.object(Appointment.objects, 'get', return_value=mock_appointment):
            result = appointment_repository.delete_appointment(appointment_id)
            mock_appointment.delete.assert_called_once()
            assert result is True

    def test_delete_appointment_not_found(self, appointment_repository):
        """Ensures delete_appointment handles Appointment.DoesNotExist correctly and returns False."""
        appointment_id = 'non-existent-id'
        with patch.object(Appointment.objects, 'get', side_effect=Appointment.DoesNotExist):
            result = appointment_repository.delete_appointment(appointment_id)
            assert result is False
