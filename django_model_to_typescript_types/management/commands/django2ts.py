import os

from django.core.management.base import BaseCommand
from ...modeltotypescriptconverter import ModelToTypeScriptConverter

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        """Handle the command"""
        converter = ModelToTypeScriptConverter(os.environ.get('TS_APP_TO_INCLUDE', 'app'), os.environ.get('TS_PATH', '/tmp/tsinterface/'), os.environ.get('TS_SEPERATED_FILES', False))
        converter.generate_interfaces()
        

