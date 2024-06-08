from django.db import IntegrityError
from services.models import Service
from services.repositories.interfaces.service_repository_interface import ServiceRepositoryInterface


class ServiceRepository(ServiceRepositoryInterface):
    def get_service_by_id(self, service_id):
        try:
            return Service.objects.get(id=service_id)
        except:
            return None
    
    def get_all_services(self):
        return Service.objects.all()
    
    def create_service(self, service_data):
        try:
            return Service.objects.create(**service_data)
        except IntegrityError:
            return None

    
    def update_service(self, service_id, service_data):
        try:
            service = Service.objects.get(id=service_id)
            for key, value in service_data.items():
                setattr(service, key, value)
            service.save()
            return service
        except Service.DoesNotExist:
            return None
        except IntegrityError:
            return None
    
    def delete_service(self, service_id):
        try:
            service = Service.objects.get(id=service_id)
            service.delete()
            return True
        except Service.DoesNotExist:
            return False
