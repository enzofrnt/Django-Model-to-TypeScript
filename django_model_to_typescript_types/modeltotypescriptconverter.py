# https://gist.github.com/emoss08/c87c9864ce2af470dc301ff64e39f857
# https://gist.github.com/guizesilva/474fce56fcd5ab766e65e11e0dbff545
import os

from django.apps import apps
from django.core.wsgi import get_wsgi_application

class ModelToTypeScriptConverter:
    def __init__(self, apps_to_include=['app'], path_for_interfaces='/tmp/tsinterface/', seperated_files=False):
        self.apps_to_include = apps_to_include.split(',')
        self.path_for_interfaces = path_for_interfaces
        if isinstance(seperated_files, str):
            self.seperated_files = seperated_files.lower() in ('true')
        else:
            self.seperated_files = bool(seperated_files)
        self.field_type_mapping = {
            "AutoField": "number",
            "BooleanField": "boolean",
            "CharField": "string",
            "DateField": "Date",
            "DateTimeField": "Date",
            "DecimalField": "number",
            "FloatField": "number",
            # "ForeignKey": "number", The foreign key is handled separately
            "IntegerField": "number",
            "JSONField": "JSON",
            "ManyToManyField": None,
            "OneToOneField": "number",
            "PositiveIntegerField": "number",
            "PositiveSmallIntegerField": "number",
            "TextField": "string",
            "UUIDField": "string",
            "BigAutoField": "number",
        }

    def get_wsgi_application(self):
        get_wsgi_application()

    def to_camel_case(self, snake_str):
        """Transform a string from snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def to_type_union(self, field):
        """Transform field options to TypeScript union type."""
        choices = field.choices
        return " | ".join([f'"{choice[0]}"' for choice in choices])

    def generate_interfaces(self):
        all_models = apps.get_models()
        os.makedirs(os.path.dirname(self.path_for_interfaces), exist_ok=True)

        if self.seperated_files:
            for model in all_models:
                if model._meta.app_label in self.apps_to_include:
                    self.generate_interface_file(model)
        else:
            self.generate_single_interface_file(all_models)

    def generate_field_line(self, field):
        if field.get_internal_type() == 'ForeignKey':
            # Handling ForeignKey specifically
            related_model = field.related_model
            print("related name of the foreign key : "+field.remote_field.related_name or f'{related_model._meta.model_name}_set')
            # You could choose to reference the primary key type of the related model
            # or simply use the related model's name as a type
            _type = related_model.__name__ + " | " + self.field_type_mapping.get(related_model._meta.pk.get_internal_type(), None)
            # Assuming we always import the related model's type at the top of the file
            needs_import = True
        else:
            _type = self.field_type_mapping.get(field.get_internal_type(), None)
            needs_import = False

        if _type is None:
            return None, needs_import

        if field.choices:
            _type = self.to_type_union(field)

        name = self.to_camel_case(field.name)
        if field.null:
            name += "?"

        return f"{name}: {_type};", needs_import

    def generate_interface_definition(self, model):
        lines = [f"export interface {model.__name__}{{\n"]
        imports_needed = set()
        for field in model._meta.fields:
            field_line, needs_import = self.generate_field_line(field)
            if field_line:
                lines.append(f"\t{field_line}\n")
                if needs_import and self.seperated_files :
                    related_model = field.related_model
                    imports_needed.add(related_model.__name__)
        header = ""
        if imports_needed:
            # Generate import lines for needed models
            for import_model in imports_needed:
                header += f"import {{ {import_model} }} from './{import_model}';\n"
            header += "\n"  # Add a newline after imports for readability
        lines.insert(0, header)
        lines.append("}\n\n")
        return "".join(lines)

    def generate_interface_file(self, model):
        with open(f"{self.path_for_interfaces}{model.__name__.lower()}.ts", "w") as file:
            print(f"Generating {model.__name__}.ts")
            file.write(self.generate_interface_definition(model))

    def generate_single_interface_file(self, all_models):
        with open(f"{self.path_for_interfaces}interfaces.ts", "w") as file:
            print("Generating interfaces.ts")
            for model in all_models:
                if model._meta.app_label in self.apps_to_include:
                    file.write(self.generate_interface_definition(model))

        