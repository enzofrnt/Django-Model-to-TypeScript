import os

from django.apps import AppConfig
from .modeltotypescriptconverter import ModelToTypeScriptConverter

class DjangoModelToTypescriptTypesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_model_to_typescript_types'

    def ready(self):
        if os.environ.get('RUN_MAIN') :
            print('Lets convert the models to typescript types')
            # converter = ModelToTypeScriptConverter(os.environ.get('TS_APP_TO_INCLUDE', 'app'), os.environ.get('TS_PATH', '/tmp/tsinterface/interfaces.ts'), os.environ.get('TS_SEPERATED_FILES', False))
            converter = ModelToTypeScriptConverter(os.environ.get('TS_APP_TO_INCLUDE', 'app'), os.environ.get('TS_PATH', '/tmp/tsinterface/'), os.environ.get('TS_SEPERATED_FILES', True))
            converter.generate_interfaces()
        

    
