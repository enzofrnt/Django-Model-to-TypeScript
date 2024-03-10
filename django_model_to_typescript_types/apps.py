import os

from django.apps import AppConfig
from .modeltotypescriptconverter import ModelToTypeScriptConverter

class DjangoModelToTypescriptTypesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_model_to_typescript_types'

    def ready(self):
        if os.environ.get('RUN_MAIN') :
            converter = ModelToTypeScriptConverter(os.environ.get('TS_APP_TO_INCLUDE', 'app'), os.environ.get('TS_PATH', '/tmp/tsinterface/'), os.environ.get('TS_SEPERATED_FILES', False), os.environ.get('DJANGO2TS_VERBOSE', False))
            converter.generate_interfaces()
        

    
