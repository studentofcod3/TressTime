from abc import ABC, abstractmethod


class AppointmentRepositoryInterface(ABC):
    @abstractmethod
    def get_appointment_by_id(self, appointment_id):
        pass

    @abstractmethod
    def get_all_appointments(self):
        pass

    @abstractmethod
    def create_appointment(self, appointment_data):
        pass

    @abstractmethod
    def update_appointment(self, appointment_id, appointment_data):
        pass

    @abstractmethod
    def delete_appointment(self, appointment_id):
        pass
