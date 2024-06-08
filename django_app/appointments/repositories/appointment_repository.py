from django.db import IntegrityError
from appointments.models import Appointment
from appointments.repositories.interfaces.appointment_repository_interface import AppointmentRepositoryInterface


class AppointmentRepository(AppointmentRepositoryInterface):
    def get_appointment_by_id(self, appointment_id):
        try:
            return Appointment.objects.get(id=appointment_id)
        except:
            return None
        
    def get_all_appointments(self):
        return Appointment.objects.all()
    
    def create_appointment(self, appointment_data):
        try:
            return Appointment.objects.create(**appointment_data)
        except IntegrityError:
            return None
        
    def update_appointment(self, appointment_id, appointment_data):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            for key, value in appointment_data.items():
                setattr(appointment, key, value)
            appointment.save()
            return appointment
        except Appointment.DoesNotExist:
            return None
        except IntegrityError:
            return None
        
    def delete_appointment(self, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return True
        except Appointment.DoesNotExist:
            return False
