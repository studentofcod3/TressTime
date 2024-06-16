import pytest
import uuid

from datetime import datetime

from django.db import IntegrityError
from django.utils.timezone import make_aware as make_aware_of_timezone

from services.models import Service


@pytest.mark.django_db
class TestServiceModel:
    """This tests the Service entity at the database level."""

    # Field values
    service_id = uuid.uuid4()
    created_at = make_aware_of_timezone(datetime.now())
    updated_at = make_aware_of_timezone(datetime.now())
    name = 'Cut, Wash and Dry'
    description = ("Indulge in our signature 'Wash, Cut & Dry' service, designed to pamper you from start to finish. "
                   "Relax and unwind as our skilled stylists begin with a soothing scalp massage during your wash, "
                   "using premium products tailored to your hair type. Enjoy a custom haircut that complements your "
                   "unique style and facial features, crafted with precision and care. Conclude your visit with a "
                   "professional blow-dry that leaves your hair silky, smooth, and beautifully styled. "
                   "Treat yourself to a refreshing experience that rejuvenates both your hair and your spirit.")
    duration = 60  # Measured in minutes
    price = 50  # Currency is GBP
    availability = True

    def test_minimal_required_fields_present(self):
        """
        Test the minimal required fields needed to create the Service entity.

        Some of the required fields have default values, this test confirms they are present post creation.
        """
        service = Service.objects.create(
            name=self.name,
            description=self.description,
            duration=self.duration,
            price=self.price
        )

        assert service.id
        assert service.created_at
        assert service.name == self.name
        assert service.description == self.description
        assert service.duration == self.duration
        assert service.price == self.price
        assert service.availability == self.availability

    @pytest.mark.parametrize(
        'service_id,created_at,updated_at,missing_value',
        [
            (None, created_at, updated_at, 'id'),
            (service_id, None, updated_at, 'created_at'),
            (service_id, created_at, updated_at, 'updated_at'),
        ]
    )
    def test_required_non_overridable_default_fields(self, service_id, created_at, updated_at, missing_value):
        """Ensure required fields with non-overridable default values are always populated.

        Certain fields are populated even if explicitly set as Null. This is an extra precaution as there is no
        scenario where this is intentionally desired.

        The current fields for which this is the case are:
        - id (primary key)
        - created_at
        - updated_at
        """
        service = Service.objects.create(
            # Required fields - Non overridable defaults
            id=service_id,
            created_at=created_at,
            updated_at=updated_at,
            # Required fields - No defaults
            name=self.name,
            description=self.description,
            duration=self.duration,
            price=self.price
        )
        assert getattr(service, missing_value)

    @pytest.mark.parametrize(
        'name,description,duration,price,availability,missing_value',
        [
            (None, description, duration, price, availability, 'name'),
            (name, None, duration, price, availability, 'description'),
            (name, description, None, price, availability, 'duration'),
            (name, description, duration, None, availability, 'price'),
            (name, description, duration, price, None, 'availability'),
        ]
    )
    def test_required_fields_missing(self, name, description, duration, price, availability, missing_value):
        """
            Each iteration attempts creation with a missing required field.

            All required fields should be tested here,
            except non-overridable default fields - those are tested in `test_required_non_overridable_default_fields`.

            To update this test with new fields:
            - Add a new parameter above, following the pattern used.
            - Add a row in the 'create' query.
        """
        with pytest.raises(IntegrityError) as missing_column_error:
            Service.objects.create(
                name=name,
                description=description,
                duration=duration,
                price=price,
                availability=availability,
            )
        assert 'violates not-null constraint' in str(missing_column_error._excinfo)
        assert f'null value in column "{missing_value}"' in str(missing_column_error)

    @pytest.mark.parametrize(
        'duplicate_id,duplicate_name,error_text',
        [
            (True, False, 'id'),
            (False, True, 'name'),
        ]
    )
    def test_unique_constraint_violated(self, duplicate_id, duplicate_name, error_text):
        """
        Each iteration attempts creation with a duplicate 'unique' field.

        ALL fields with the 'unique' constraint set should be tested here.

        To update this test with new fields:
        - Add a new parameter above, following the boolean pattern used.
        - Add a new entry in the 'Unique fields' section below.
        - Add a row in the 'create' query.
        """
        service = Service.objects.create(
            name=self.name,
            description=self.description,
            duration=self.duration,
            price=self.price
        )
        # Unique fields
        service_id = service.id if duplicate_id else uuid.uuid4()
        name = service.name if duplicate_name else 'A different name'

        with pytest.raises(IntegrityError) as unique_contraint_violation_error:
            Service.objects.create(
                pk=service_id,
                name=name,
                description=self.description,
                duration=self.duration,
                price=self.price
            )

        assert "duplicate key value violates unique constraint" in str(unique_contraint_violation_error)
        assert (f"Key ({error_text})=({getattr(service, error_text)}) already exists"
                in str(unique_contraint_violation_error))
