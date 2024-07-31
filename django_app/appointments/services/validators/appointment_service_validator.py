import re

from datetime import datetime
from django.core.exceptions import ValidationError

from appointments.repositories.appointment_repository import AppointmentRepository

class AppointmentServiceValidator:
    """
    Validates the business logic for the Appointment entity.

    Methods:
        validate_appointment_data(appointment_data, is_update=False)
        validate_created_at(created_at)
        validate_updated_at(updated_at)
        
    """
    ALLOWED_APPOINTMENT_STATUSES = ["scheduled", "completed", "canceled"]

    def __init__(self):
        self.appointment_repository = AppointmentRepository()

    def validate_appointment_exists(self, appointment, appointment_id):
        if not appointment:
            raise ValidationError(f"Appointment with ID {appointment_id} does not exist.")

    def validate_appointment_data(self, appointment_data, is_update=False):
        """
        Validates appointment data.
        
        This contains any business logic validation (e.g., string length, value ranges, format checks).
        Any database level constraints (e.g., unique constraints, field types, nullability) should be defined on the model.
        """
        if is_update:
            if 'id' in appointment_data:
                raise ValidationError("ID cannot be modified.")
            self.validate_updated_at(updated_at=appointment_data.get('updated_at', None))
        else:
            self.validate_created_at(created_at=appointment_data.get('created_at', None))
            self.validate_updated_at(updated_at=appointment_data.get('updated_at', None))
        self.validate_starts_at_ends_at(
            starts_at=appointment_data.get('starts_at', None),
            ends_at=appointment_data.get('ends_at', None)
        )
        self.validate_status(status=appointment_data.get('status', None))
        self.validate_confirmation_number(
            confirmation_number=appointment_data.get('confirmation_number', None),
            appointment_id=appointment_data.get('id', None)
        )

    def validate_created_at(self, created_at):
        # TODO: move created/updated validation to a 'common' module used in all apps
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
        
    def validate_starts_at_ends_at(self, starts_at, ends_at):
        """Validate the start and end time for the appointment."""
        if starts_at is None or ends_at is None:
            raise ValidationError("Both starts_at and ends_at are required.")
        if not isinstance(starts_at, datetime) or not isinstance(ends_at, datetime):
            raise ValidationError("Both starts_at and ends_at must be datetime objects")
        is_starts_at_unaware = starts_at.tzinfo is None or starts_at.tzinfo.utcoffset(starts_at) is None
        is_ends_at_unaware = ends_at.tzinfo is None or ends_at.tzinfo.utcoffset(ends_at) is None
        if is_starts_at_unaware or is_ends_at_unaware:
            raise ValidationError("Both starts_at and ends_at must be aware datetime objects with timezone information.")
        if starts_at > ends_at:
            raise ValidationError("End time cannot be earlier than end time")


    def validate_status(self, status):
        """
        Validate status of the appointment.

        Options are 'scheduled', 'completed', 'canceled'.
        """
        if not status:
            raise ValidationError("status is required.")
        if status not in self.ALLOWED_APPOINTMENT_STATUSES:
            allowed_statuses_str = ", ".join(self.ALLOWED_APPOINTMENT_STATUSES)
            raise ValidationError(f"status must be one of the following: {allowed_statuses_str}")

    def validate_confirmation_number(self, confirmation_number, appointment_id):
        """
        Validate the confirmation number for the appointment
        """
        if confirmation_number:
            # Validate confirmation_number is unique
            appointment_queryset = self.appointment_repository.get_appointment_by_confirmation_number(confirmation_number)
            appointment_list = list(appointment_queryset.values_list('id', flat=True))
            appointment_str = ", ".join([str(appointment) for appointment in appointment_list])
            if len(appointment_list) > 1:
                # This could occur if someone bypassed the service layer and manually updated the DB, this would be an edge case.
                raise ValidationError(f"Multiple appointments ({str(appointment_str)}) with same confirmation number. Confirmation number must be unique")
            appointment = appointment_list[0]
            if appointment and appointment.id != appointment_id:
                # This is more likely to be triggered than the above, this is if the system tries to create a new confirmation number which already exists.
                raise ValidationError(f"Appointment with confirmation number already exists ({appointment_str}). Confirmation number must be unique")
            # Validate confirmation_number is 9 digits
            if len(confirmation_number) != 9:
                raise ValidationError("confirmation number must be 9 digits long")
