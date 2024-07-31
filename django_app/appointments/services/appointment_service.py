from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware as make_aware_of_timezone

from appointments.repositories.appointment_repository import AppointmentRepository
from appointments.services.interfaces.appointment_service_interface import AppointmentServiceInterface
from appointments.services.validators.appointment_service_validator import AppointmentServiceValidator



class AppointmentService(AppointmentServiceInterface):
    """
    AppointmentService class handles the business logic for the Appointment entity.

    Methods:
        get_appointment(appointment_id)
        get_all_appointments()
        create_appointment(appointment_data)
        update_appointment(appointment_id, appointment_data)
        delete_appointment(appointment_id)
    """
    def __init__(self):
        self.appointment_repository = AppointmentRepository()
        self.validator = AppointmentServiceValidator()

    def get_appointment(self, appointment_id):
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        self.validator.validate_appointment_exists(appointment, appointment_id)
        return appointment
    
    def get_all_appointments(self):
        appointments = self.appointment_repository.get_all_appointments()
        return appointments

    def create_appointment(self, appointment_data):
        appointment_data['created_at'] = make_aware_of_timezone(datetime.now())
        appointment_data['updated_at'] = make_aware_of_timezone(datetime.now())
        self.validator.validate_appointment_data(appointment_data)
        try:
            self.appointment_repository.create_appointment(appointment_data)
        except Exception as e:
            raise ValidationError(f"Error creating appointment: {e}")

    def update_appointment(self, appointment_id, appointment_data):
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        self.validator.validate_appointment_exists(appointment, appointment_id)
        # Set updated_at timestamp and validate data before updating.
        appointment_data['updated_at'] = make_aware_of_timezone(datetime.now())
        self.validator.validate_appointment_data(appointment_data, is_update=True)
        try:
            return self.appointment_repository.update_appointment(appointment_id, appointment_data)
        except Exception as e:
            raise ValidationError(f"Error updating appointment: {e}")

    def delete_appointment(self, appointment_id):
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        self.validator.validate_appointment_exists(appointment, appointment_id)
        try:
            return self.appointment_repository.delete_appointment(appointment_id)
        except Exception as e:
            raise ValidationError(f"Error deleting appointment: {e}")