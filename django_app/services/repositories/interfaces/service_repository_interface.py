from abc import ABC, abstractmethod


class ServiceRepositoryInterface(ABC):
    @abstractmethod
    def get_service_by_id(self, service_id):
        pass

    @abstractmethod
    def get_all_services(self):
        pass

    @abstractmethod
    def create_service(self, service_data):
        pass

    @abstractmethod
    def update_service(self, service_id, service_data):
        pass

    @abstractmethod
    def delete_service(self, service_id):
        pass
