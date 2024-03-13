from django.core.management.base import BaseCommand
from ...modeltotypescriptconverter import ModelToTypeScriptConverter

class Command(BaseCommand):
    help = "Convert Django Models to TypeScript Models"

    def add_arguments(self, parser):
        parser.add_argument('--apps', default='app', help='Comma separated list of apps to include')
        parser.add_argument('--path', default='/tmp/tsinterface/', help='Path for the TypeScript interfaces')
        parser.add_argument('--exclude-models', default='', help='Comma separated list of models to exclude')
        parser.add_argument('--exclude-fields', default='', help='Comma separated list of fields to exclude')
        parser.add_argument('--files', action='store_true', help='Generate separated files for each model')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def handle(self, *args, **options):
        apps_to_include = options['apps']
        path_for_interfaces = options['path']
        excluded_models = options['exclude_models']
        excluded_fields = options['exclude_fields']
        separated_files = options['files']
        verbose = options['verbose']

        converter = ModelToTypeScriptConverter(apps_to_include, path_for_interfaces, excluded_models, excluded_fields, separated_files, verbose)
        converter.generate_interfaces()