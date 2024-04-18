# TressTime frontend

The frontend code of this project is housed in this module. 

The reason for keeping this outside the django_app module is to keep the backend and frontend decoupled, 
making it easier to maintain, scale and even switch out the backend frontend. Only the final build resides in the 
django-app module (within the nested frontend module)   