import os

from django.apps import AppConfig
from .modeltotypescriptconverter import ModelToTypeScriptConverter

class DjangoModelToTypescriptTypesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_model_to_typescript_types'

    def ready(self):
        if os.environ.get('RUN_MAIN') :
            print('Lets convert the models to typescript types')
            converter = ModelToTypeScriptConverter()
            converter.generate_interfaces()
        

    
