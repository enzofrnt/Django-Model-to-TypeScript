# https://gist.github.com/emoss08/c87c9864ce2af470dc301ff64e39f857
# https://gist.github.com/guizesilva/474fce56fcd5ab766e65e11e0dbff545
import os
import argparse
import sys
import importlib

from django.apps import apps
from django.core.wsgi import get_wsgi_application
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

class ModelToTypeScriptConverter:
    def __init__(self, apps_to_include=['app'], path_for_interfaces='/tmp/tsinterface/', excluded_models='', excluded_fields='', separated_files=False, verbose=False):
        self.apps_to_include = apps_to_include.split(',') 
        self.path_for_interfaces = path_for_interfaces
        self.excluded_models = excluded_models.split(',')
        self.excluded_fields = excluded_fields.split(',')
        self.separated_files = separated_files if isinstance(separated_files, bool) else separated_files.lower() in ('true', '1', 't')
        self.field_type_mapping = {
            "AutoField": "number",
            "BooleanField": "boolean",
            "CharField": "string",
            "DateField": "Date",
            "DateTimeField": "Date",
            "DecimalField": "number",
            "FloatField": "number",
            # ForeignKey is handled separately
            "IntegerField": "number",
            "JSONField": "JSON",
            # ManyToManyField and OneToOneField are handled separately
            "PositiveIntegerField": "number",
            "PositiveSmallIntegerField": "number",
            "TextField": "string",
            "UUIDField": "string",
            "BigAutoField": "number",
        }
        # self.field_type_mapping.update(extra_fields_to_ts)
        self.verbose = verbose        
        self.model_relations = {}

    def get_wsgi_application(self):        
        current_folder = os.getcwd()
        if current_folder not in sys.path:
            sys.path.append(current_folder)
        modules = [f[:-3] for f in os.listdir(current_folder) if f.endswith('.py') and not f.startswith('__')]
        for module in modules:
            globals()[module] = importlib.import_module(module)
        get_wsgi_application()

    def to_camel_case(self, snake_str):
        components = snake_str.split("_")
        return components[0] + ''.join(x.title() for x in components[1:])

    def to_type_union(self, field):
        choices = field.choices
        return ' | '.join([f'"{choice[0]}"' for choice in choices])

    def collect_model_relations(self, all_models):
        """Collects relations for each model to handle related_names in interfaces."""
        for model in all_models:
            if model._meta.app_label not in self.apps_to_include or model.__name__ in self.excluded_models:
                continue

            for field in model._meta.fields + model._meta.many_to_many:
                if field.name in self.excluded_fields :
                    continue
                if hasattr(field, 'remote_field') and field.remote_field:
                    related_model = field.related_model
                    related_name = field.remote_field.related_name or f'{model._meta.model_name}_set'
                    if related_model not in self.model_relations:
                        self.model_relations[related_model] = []
                    self.model_relations[related_model].append((model, related_name))

    def generate_interface_file(self, model):
        filename = f"{self.path_for_interfaces}{model.__name__.lower()}.ts"
        with open(filename, "w") as file:
            file.write(self.generate_interface_definition(model))

    def generate_interface_definition(self, model):
        lines = [f"export interface {model.__name__} {{\n"]
        imports_needed = set()

        # Generate field lines
        for field in model._meta.fields + model._meta.many_to_many:
            if field.name in self.excluded_fields:
                continue
            field_line, needs_import = self.generate_field_line(field)
            if field_line:
                lines.append(f"\t{field_line}\n")
                if needs_import and self.separated_files:
                    related_model = field.related_model
                    imports_needed.add(related_model.__name__)

        # Add related names as optional fields
        if model in self.model_relations:
            for related_model, related_name in self.model_relations[model]:
                type_name = related_model.__name__
                type_name = type_name + "[] | " + self.field_type_mapping.get(related_model._meta.pk.get_internal_type(), None) + "[]"
                lines.append(f"\t{self.to_camel_case(related_name)}?: {type_name};\n")

        # Handle imports
        header = ""
        if imports_needed:
            for import_model in imports_needed:
                header += f"import {{ {import_model} }} from './{import_model.lower()}';\n"
            header += "\n"
        lines.insert(0, header)
        lines.append("}\n\n")
        return "".join(lines)

    def generate_field_line(self, field):
        if field.get_internal_type() in ['ForeignKey', 'OneToOneField']:
            related_model = field.related_model
            _type = related_model.__name__ + " | " + self.field_type_mapping.get(related_model._meta.pk.get_internal_type(), None)
            needs_import = True
        elif field.get_internal_type() == 'ManyToManyField':
            related_model = field.related_model
            _type = f"{related_model.__name__}[]" + " | " + self.field_type_mapping.get(related_model._meta.pk.get_internal_type(), None) + "[]"
            needs_import = True
        else:
            _type = self.field_type_mapping.get(field.get_internal_type(), "any")
            needs_import = False

        if field.choices:
            _type = self.to_type_union(field)

        name = self.to_camel_case(field.name)
        if field.null or field.get_internal_type() in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
            name += "?"

        return f"{name}: {_type};", needs_import
    
    def generate_single_interface_file(self, all_models):
        with Progress(
            TextColumn("[bold green]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None, complete_style="green", finished_style="green"), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            expand=True
        ) as progress:
            generate_ts_models = progress.add_task("[red]Converting Django Models to TypeScript Models...", total=len(all_models), filename="interfaces.ts")
            filename = f"{self.path_for_interfaces}interfaces.ts"
            with open(filename, "w") as file:
                print("Generating interfaces.ts")
                for model in all_models:
                    file.write(self.generate_interface_definition(model))
                    progress.update(generate_ts_models, advance=1)

    def generate_interfaces(self, in_django_app=True):
        if not in_django_app:
            self.get_wsgi_application()
        
        
        all_models = [model for model in apps.get_models() if model._meta.app_label in self.apps_to_include]
        nb_models = len(all_models)

        if nb_models == 0:
            print("No models found.")
            return
        
        print("Generating TypeScript interfaces...")
        print(f"{nb_models} models found.")

        os.makedirs(os.path.dirname(self.path_for_interfaces), exist_ok=True)
        
        self.collect_model_relations(all_models)

        if self.separated_files:
            with Progress(
                TextColumn("[bold green]Processing", justify="right"),
                BarColumn(bar_width=None, complete_style="green", finished_style="green"), 
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeRemainingColumn(),
                expand=True
            ) as progress:
                generate_ts_models = progress.add_task("[red]Converting Django Models to TypeScript Models...", total=len(all_models))
                for model in all_models:
                    if model.__name__ in self.excluded_models:
                        continue
                    filename = model.__name__.lower() + ".ts"
                    progress.console.print(f"Generating {filename}")
                    self.generate_interface_file(model)
                    progress.update(generate_ts_models, advance=1)
        else:
            self.generate_single_interface_file(all_models)

def main():
    # Configuration du parseur d'arguments
    parser = argparse.ArgumentParser(description='Convert Django Models to TypeScript Models')
    parser.add_argument('--apps', default='app', help='Comma separated list of apps to include')
    parser.add_argument('--path', default='/tmp/tsinterface/', help='Path for the TypeScript interfaces')
    parser.add_argument('--exclude-models', default='', help='Comma separated list of models to exclude')
    parser.add_argument('--exclude-fields', default='', help='Comma separated list of fields to exclude')
    # parser.add_argument('--extra-fields-to-ts', default='', help='Extra fields to add to the mapping')
    parser.add_argument('--files', action='store_true', help='Generate separated files for each model')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    # Conversion des arguments de ligne de commande
    apps_to_include = args.apps_to_include
    path_for_interfaces = args.path_for_interfaces
    excluded_models = args.excluded_models
    excluded_fields = args.excluded_fields
    # extra_fields_to_ts = args.extra_fields_to_ts
    separated_files = args.separated_files
    verbose = args.verbose

    # Création et exécution du convertisseur
    converter = ModelToTypeScriptConverter(apps_to_include, path_for_interfaces, excluded_models, excluded_fields, separated_files, verbose)
    converter.generate_interfaces(in_django_app=False)

if __name__ == "__main__":
    main()

        