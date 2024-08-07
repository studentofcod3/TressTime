
from datetime import datetime, timedelta
import uuid
from django.db import IntegrityError
from django.utils.timezone import make_aware as make_aware_of_timezone
import pytest

from appointments.models import Appointment
from services.models import Service
from users.models import CustomUser
from notifications.models import Notification

@pytest.mark.django_db
class TestNotification:
    """This tests the Notification entity at the database level."""
    # Field values - Generic
    created_at = make_aware_of_timezone(datetime.now())
    updated_at = make_aware_of_timezone(datetime.now())

    # Field values - Notification entity
    notification_id = uuid.uuid4()
    notification_type = 'test_type'
    notification_status = 'test_status'
    notification_message = 'test message'
    notification_scheduled_send_datetime = make_aware_of_timezone(datetime.now())
    notification_priority = 'test_priority'

    # Field values - Dependency objects:
    ## User
    username = 'test_username'
    email = 'test_email'
    password = 'test_password'
    ## Service
    name = 'Test Service Name'
    description = 'Test Service Description'
    duration = 60
    price = 50
    ## Appointment
    starts_at = make_aware_of_timezone(datetime.now() + timedelta(days=1))
    ends_at = make_aware_of_timezone(datetime.now() + timedelta(days=1, hours=1))
    appointment_status = 'test_status'

    def create_notification_entity_dependencies(self):
        """
        Creates the required foreign entities to allow notification entity creation.

        Returns: User
        """

        user = CustomUser.objects.create(
            created_at=self.created_at,
            updated_at=self.updated_at,
            username=self.username,
            email=self.email,
            password=self.password
        )

        return user
    
    def test_minimal_required_fields_present(self):
        """
        Test the minimal fields needed to create the Notification entity.

        Some of the required fields have default values, this test confirms they are present post creation.
        """
        user = self.create_notification_entity_dependencies()
        notification = Notification.objects.create(
            type=self.notification_type,
            status=self.notification_status,
            message=self.notification_message,
            scheduled_send_datetime=self.notification_scheduled_send_datetime,
            priority=self.notification_priority,
            user=user
        )
        assert notification.id
        assert notification.created_at
        assert notification.type == self.notification_type
        assert notification.status == self.notification_status
        assert notification.message == self.notification_message
        assert notification.scheduled_send_datetime == self.notification_scheduled_send_datetime
        assert notification.priority == self.notification_priority
        assert notification.user == user

    @pytest.mark.parametrize(
            'notification_id,created_at,updated_at,missing_value',
            [
                (None,created_at,updated_at, 'id'),
                (notification_id,None,updated_at, 'created_at'),
                (notification_id,created_at,None, 'updated_at'),
            ]
    )
    def test_required_non_overridable_default_fields(self, notification_id, created_at, updated_at, missing_value):
        """Ensure required fields with non-overridable default values are always populated.

        Certain fields are populated even if explicitly set as Null. This is an extra precaution as there is no
        scenario where this is intentionally desired.

        The current fields for which this is the case are:
        - id (primary key)
        - created_at
        - updated_at
        """
        user = self.create_notification_entity_dependencies()

        notification = Notification.objects.create(
            # Required fields - Non overridable defaults
            id=notification_id,
            created_at=created_at,
            updated_at=updated_at,
            # Required fields - No defaults
            type=self.notification_type,
            status=self.notification_status,
            message=self.notification_message,
            scheduled_send_datetime=self.notification_scheduled_send_datetime,
            priority=self.notification_priority,
            user=user,
        )
        assert getattr(notification, missing_value)

    @pytest.mark.parametrize(
            'notification_type,notification_status,notification_message,notification_scheduled_send_datetime,\
                notification_priority,existing_user,missing_value',
            [
                (None,notification_status,notification_message,notification_scheduled_send_datetime,notification_priority,True,'type'),
                (notification_type,None,notification_message,notification_scheduled_send_datetime,notification_priority,True,'status'),
                (notification_type,notification_status,None,notification_scheduled_send_datetime,notification_priority,True,'message'),
                (notification_type,notification_status,notification_message,None,notification_priority,True,'scheduled_send_datetime'),
                (notification_type,notification_status,notification_message,notification_scheduled_send_datetime,None,True,'priority'),
                (notification_type,notification_status,notification_message,notification_scheduled_send_datetime,notification_priority,False,'user_id'),
            ]
    )
    def test_required_fields_missing(
            self, 
            notification_type, 
            notification_status, 
            notification_message, 
            notification_scheduled_send_datetime, 
            notification_priority, 
            existing_user, 
            missing_value
            ):
        """
            Each iteration attempts creation with a missing required field (foreign keys inclusive).

            All required fields should be tested here,
            except non-overridable default fields - those are tested in `test_required_non_overridable_default_fields`.

            To update this test with new fields:
            - Add a new parameter above, following the pattern used.
            - Add a row in the 'create' query.
        """
        user = self.create_notification_entity_dependencies()
        user = user if existing_user else None

        with pytest.raises(IntegrityError) as missing_column_error:
            Notification.objects.create(
                type=notification_type,
                status=notification_status,
                message=notification_message,
                scheduled_send_datetime=notification_scheduled_send_datetime,
                priority=notification_priority,
                user=user,
            )
        assert 'violates not-null constraint' in str(missing_column_error._excinfo)
        assert f'null value in column "{missing_value}"' in str(missing_column_error)

    def test_unique_constraint_violated(self):
        """
        Attempts creation with a duplicate 'unique' field.

        ALL fields with the 'unique' constraint set should be tested here (currently, this is just the primary key).
        """
        user = self.create_notification_entity_dependencies()
        notification = Notification.objects.create(
            type=self.notification_type,
            status=self.notification_status,
            message=self.notification_message,
            scheduled_send_datetime=self.notification_scheduled_send_datetime,
            priority=self.notification_priority,
            user=user,
        )

        with pytest.raises(IntegrityError) as unique_contraint_violation_error:
            Notification.objects.create(
                # Tested fields
                pk=notification.id,
                # Non-tested fields needed for object creation
                type=self.notification_type,
                status=self.notification_status,
                message=self.notification_message,
                scheduled_send_datetime=self.notification_scheduled_send_datetime,
                priority=self.notification_priority,
                user=user,
            )
        
        assert "duplicate key value violates unique constraint" in str(unique_contraint_violation_error)
        assert (f"Key (id)=({getattr(notification, 'id')}) already exists"
                in str(unique_contraint_violation_error))

    def test_optional_relationship(self):
        """Test that any optional relationships are correctly added upon creation"""
        user = self.create_notification_entity_dependencies()
        service = Service.objects.create(
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            description=self.description,
            duration=self.duration,
            price=self.price
        )
        appointment = Appointment.objects.create(
            created_at=self.created_at,
            updated_at=self.updated_at,
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            status=self.appointment_status,
            user=user,
            service=service,
        )
        notification = Notification.objects.create(
            type=self.notification_type,
            status=self.notification_status,
            message=self.notification_message,
            scheduled_send_datetime=self.notification_scheduled_send_datetime,
            priority=self.notification_priority,
            user=appointment.user,
            appointment=appointment
        )
        assert notification.appointment == appointment
        assert notification.user == user
        assert notification.appointment.service == service
