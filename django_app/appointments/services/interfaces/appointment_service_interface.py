from abc import ABC, abstractmethod


class AppointmentServiceInterface(ABC):
    @abstractmethod
    def get_appointment(self, apointment_id):
        pass

    @abstractmethod
    def get_all_appointments(self):
        pass

    @abstractmethod
    def create_appointment(self, apointment_data):
        pass

    @abstractmethod
    def update_appointment(self, apointment_id, apointment_data):
        pass

    @abstractmethod
    def delete_appointment(self, apointment_id):
        pass
