import uuid
from datetime import datetime

import pytest
from django.db import IntegrityError
from django.utils.timezone import make_aware as make_aware_of_timezone

from users.models import CustomUser


@pytest.mark.django_db
class TestCustomUserModel:
    """This tests the User entity at the database level."""

    # Field values
    user_id = uuid.uuid4()
    created_at = make_aware_of_timezone(datetime.now())
    updated_at = make_aware_of_timezone(datetime.now())
    username = 'test_username'
    email = 'test_email'
    password = 'test_password'
    date_joined = make_aware_of_timezone(datetime.now())
    is_active = False
    is_staff = True
    is_superuser = True

    def test_minimal_required_fields_present(self):
        """
        Test the minimal required fields needed to create the User entity.

        Some of the required fields have default values, this test confirms they are present post creation.
        """
        custom_user = CustomUser.objects.create(
            created_at=self.created_at,
            updated_at=self.updated_at,
            username=self.username,
            email=self.email,
            password=self.password
        )

        assert custom_user.id
        assert custom_user.created_at
        assert custom_user.username == self.username
        assert custom_user.email == self.email
        assert custom_user.password == self.password
        assert custom_user.first_name == ''
        assert custom_user.last_name == ''
        assert custom_user.date_joined
        assert custom_user.is_active
        assert not custom_user.is_staff
        assert not custom_user.is_superuser

    @pytest.mark.parametrize(
        'user_id,missing_value',
        [
            (None, 'id'),
        ]
    )
    def test_required_non_overridable_default_fields(
            self,
            user_id,
            missing_value
    ):
        """Ensure required fields with non-overridable default values are always populated.

        Certain fields are populated even if explicitly set as Null. This is an extra precaution as there is no
        scenario where this is intentionally desired.

        The current fields for which this is the case are:
        - id (primary key)
        """
        custom_user = CustomUser.objects.create(
            # Required fields - Non overridable defaults
            id=user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            # Required fields - No defaults
            username=self.username,
            email=self.email,
            password=self.password,
        )
        assert getattr(custom_user, missing_value)

    @pytest.mark.parametrize(
        'created_at,updated_at,username,email,password,date_joined,is_active,is_staff,is_superuser,missing_value',
        [
            (None, updated_at, username, email, password, date_joined, is_active, is_staff, is_superuser, 'created_at'),
            (created_at, None, username, email, password, date_joined, is_active, is_staff, is_superuser, 'updated_at'),
            (created_at, updated_at, None, email, password, date_joined, is_active, is_staff, is_superuser, 'username'),
            (created_at, updated_at, username, None, password, date_joined, is_active, is_staff, is_superuser, 'email'),
            (created_at, updated_at, username, email, None, date_joined, is_active, is_staff, is_superuser, 'password'),
            (created_at, updated_at, username, email, password, None, is_active, is_staff, is_superuser, 'date_joined'),
            (created_at, updated_at, username, email, password, date_joined, None, is_staff, is_superuser, 'is_active'),
            (created_at, updated_at, username, email, password, date_joined, is_active, None, is_superuser, 'is_staff'),
            (created_at, updated_at, username, email, password, date_joined, is_active, is_staff, None, 'is_superuser'),
        ]
    )
    def test_required_fields_missing(
            self,
            created_at,
            updated_at,
            username,
            email,
            password,
            date_joined,
            is_active,
            is_staff,
            is_superuser,
            missing_value
    ):
        """
        Each iteration attempts creation with a missing required field.

        All required fields should be tested here,
        except non-overridable default fields - those are tested in `test_required_non_overridable_default_fields`.

        To update this test with new fields:
        - Add a new parameter above, following the pattern used.
        - Add a row in the 'create' query.
        """
        with pytest.raises(IntegrityError) as missing_column_error:
            CustomUser.objects.create(
                created_at=created_at,
                updated_at=updated_at,
                username=username,
                email=email,
                password=password,
                date_joined=date_joined,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser,
            )
        assert 'violates not-null constraint' in str(missing_column_error._excinfo)
        assert f'null value in column "{missing_value}"' in str(missing_column_error)

    @pytest.mark.parametrize(
        'duplicate_id,duplicate_username,duplicate_email,error_text',
        [
            (True, False, False, 'id'),
            (False, True, False, 'username'),
            (False, False, True, 'email'),
        ]
    )
    def test_unique_constraint_violated(
            self,
            duplicate_id,
            duplicate_username,
            duplicate_email,
            error_text
    ):
        """
        Each iteration attempts creation with a duplicate 'unique' field.

        ALL fields with the 'unique' constraint set should be tested here.

        To update this test with new fields:
        - Add a new parameter above, following the boolean pattern used.
        - Add a new entry in the 'Unique fields' section below.
        - Add a row in the 'create' query.
        """
        custom_user = CustomUser.objects.create(
            created_at=self.created_at,
            updated_at=self.updated_at,
            username=self.username,
            email=self.email,
            password=self.password
        )
        # Unique fields
        user_id = custom_user.id if duplicate_id else uuid.uuid4()
        username = custom_user.username if duplicate_username else "A different username"
        email = custom_user.email if duplicate_email else "A different email"
        # Required (non-auto) field needed for the test to run
        password = custom_user.password

        with pytest.raises(IntegrityError) as unique_contraint_violation_error:
            CustomUser.objects.create(
                created_at=self.created_at,
                updated_at=self.updated_at,
                pk=user_id,
                username=username,
                email=email,
                password=password
            )

        assert "duplicate key value violates unique constraint" in str(unique_contraint_violation_error)
        assert (f"Key ({error_text})=({getattr(custom_user, error_text)}) already exists"
                in str(unique_contraint_violation_error))
