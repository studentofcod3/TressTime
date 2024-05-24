from datetime import datetime, timedelta
import uuid
from django.db import IntegrityError
import pytest

from django.utils.timezone import make_aware as make_aware_of_timezone

from appointments.models import Appointment
from services.models import Service
from users.models import CustomUser


@pytest.mark.django_db
class TestAppointment:
    """This tests the Appointment entity at the database level"""

    # Field values
    appointment_id = uuid.uuid4()
    created_at = make_aware_of_timezone(datetime.now())
    updated_at = make_aware_of_timezone(datetime.now())
    starts_at = make_aware_of_timezone(datetime.now() + timedelta(days=1))
    ends_at = make_aware_of_timezone(datetime.now() + timedelta(days=1, hours=1))
    status = 'test_status'
    confirmation_number = 123456789

    # Field values for dependency objects:
    # User
    username = 'test_username'
    email = 'test_email'
    password = 'test_password'
    # Service
    name = 'Test Service Name'
    description = 'Test Service Description'
    duration = 60
    price = 50
    
    def create_appointment_entity_dependencies(self):
        """
        Creates the required foreign entities to allow appointment entity creation.

        Returns: User, Service
        """

        user = CustomUser.objects.create(
            username=self.username,
            email=self.email,
            password=self.password
        )
        service = Service.objects.create(
            name=self.name,
            description=self.description,
            duration=self.duration,
            price=self.price
        )
        return user, service

    def test_minimal_required_fields_present(self):
        """
        Test the minimal fields needed to create the Appointment entity.

        Some of the required fields have default values, this test confirms they are present post creation.
        """
        user, service = self.create_appointment_entity_dependencies()

        appointment = Appointment.objects.create(
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            status=self.status,
            user=user,
            service=service,
        )

        assert appointment.id
        assert appointment.created_at
        assert appointment.starts_at == self.starts_at
        assert appointment.ends_at == self.ends_at
        assert appointment.status == self.status
        assert appointment.user == user
        assert appointment.service == service

    @pytest.mark.parametrize(
            'appointment_id,created_at,updated_at,missing_value',
            [
                (None,created_at,updated_at, 'id'),
                (appointment_id,None,updated_at, 'created_at'),
                (appointment_id,created_at,None, 'updated_at'),
            ]
    )
    def test_required_non_overridable_default_fields(self, appointment_id, created_at, updated_at, missing_value):
        """Ensure required fields with non-overridable default values are always populated.

        Certain fields are populated even if explicitly set as Null. This is an extra precaution as there is no
        scenario where this is intentionally desired.

        The current fields for which this is the case are:
        - id (primary key)
        - created_at
        - updated_at
        """
        user, service = self.create_appointment_entity_dependencies()

        appointment = Appointment.objects.create(
            # Required fields - Non overridable defaults
            id=appointment_id,
            created_at=created_at,
            updated_at=updated_at,
            # Required fields - No defaults
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            status=self.status,
            user=user,
            service=service,
        )
        assert getattr(appointment, missing_value)


    @pytest.mark.parametrize(
            'starts_at,ends_at,status,existing_user,existing_service,missing_value',
            [
                (None,ends_at,status,True,True,'starts_at'),
                (starts_at,None,status,True,True,'ends_at'),
                (starts_at,ends_at,None,True,True,'status'),
                (starts_at,ends_at,status,False,True,'user_id'),
                (starts_at,ends_at,status,True,False,'service_id'),
            ]
    )
    def test_required_fields_missing(self, starts_at, ends_at, status, existing_user, existing_service, missing_value):
        """
            Each iteration attempts creation with a missing required field (foreign keys inclusive).

            All required fields should be tested here,
            except non-overridable default fields - those are tested in `test_required_non_overridable_default_fields`.

            To update this test with new fields:
            - Add a new parameter above, following the pattern used.
            - Add a row in the 'create' query.
        """
        user, service = self.create_appointment_entity_dependencies()
        user = user if existing_user else None
        service = service if existing_service else None

        with pytest.raises(IntegrityError) as missing_column_error:
            Appointment.objects.create(
                starts_at=starts_at,
                ends_at=ends_at,
                status=status,
                user=user,
                service=service,
            )
        assert 'violates not-null constraint' in str(missing_column_error._excinfo)
        assert f'null value in column "{missing_value}"' in str(missing_column_error)

    @pytest.mark.parametrize(
            'duplicate_id,duplicate_confirmation_number,error_text',
            [
                (True, False, 'id'),
                (False, True, 'confirmation_number'),
            ]
    )
    def test_unique_constraint_violated(self, duplicate_id, duplicate_confirmation_number, error_text):
        """
        Each iteration attempts creation with a duplicate 'unique' field.

        ALL fields with the 'unique' constraint set should be tested here.

        To update this test with new fields:
        - Add a new parameter above, following the boolean pattern used.
        - Add a new entry in the 'Unique fields' section below.
        - Add a row in the 'create' query.
        """
        user, service = self.create_appointment_entity_dependencies()

        appointment = Appointment.objects.create(
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            status=self.status,
            confirmation_number=self.confirmation_number,
            user=user,
            service=service,
        )
        # Unique fields
        appointment_id = appointment.id if duplicate_id else uuid.uuid4()
        confirmation_number = appointment.confirmation_number if duplicate_confirmation_number else 987654321

        with pytest.raises(IntegrityError) as unique_contraint_violation_error:
            Appointment.objects.create(
                # Tested fields
                pk=appointment_id,
                confirmation_number=confirmation_number,
                # Non-tested fields needed for object creation
                starts_at=self.starts_at,
                ends_at=self.ends_at,
                status=self.status,
                user=user,
                service=service,
            )

        assert "duplicate key value violates unique constraint" in str(unique_contraint_violation_error)
        assert (f"Key ({error_text})=({getattr(appointment, error_text)}) already exists"
                in str(unique_contraint_violation_error))
