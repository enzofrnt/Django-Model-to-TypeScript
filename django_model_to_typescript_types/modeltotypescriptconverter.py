# https://gist.github.com/emoss08/c87c9864ce2af470dc301ff64e39f857
# https://gist.github.com/guizesilva/474fce56fcd5ab766e65e11e0dbff545
import os
from django.apps import apps
from django.core.wsgi import get_wsgi_application

class ModelToTypeScriptConverter:
    def __init__(self, apps_to_include=['app'], path_for_interfaces='/tmp/tsinterface/', separated_files=False):
        self.apps_to_include = apps_to_include.split(',')
        self.path_for_interfaces = path_for_interfaces
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
        # New attribute to keep track of model relationships
        self.model_relations = {}

    def get_wsgi_application(self):
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
            if model._meta.app_label not in self.apps_to_include:
                continue

            for field in model._meta.fields + model._meta.many_to_many:
                if hasattr(field, 'remote_field') and field.remote_field:
                    related_model = field.related_model
                    related_name = field.remote_field.related_name or f'{model._meta.model_name}_set'
                    if related_model not in self.model_relations:
                        self.model_relations[related_model] = []
                    self.model_relations[related_model].append((model, related_name))

    def generate_interface_file(self, model):
        filename = f"{self.path_for_interfaces}{model.__name__.lower()}.ts"
        with open(filename, "w") as file:
            print(f"Generating {model.__name__}.ts")
            file.write(self.generate_interface_definition(model))

    def generate_interface_definition(self, model):
        lines = [f"export interface {model.__name__} {{\n"]
        imports_needed = set()

        # Generate field lines
        for field in model._meta.fields + model._meta.many_to_many:
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

    def generate_interfaces(self):
        all_models = apps.get_models()
        os.makedirs(os.path.dirname(self.path_for_interfaces), exist_ok=True)
        
        # Collect relationships between models
        self.collect_model_relations(all_models)

        if self.separated_files:
            for model in all_models:
                if model._meta.app_label in self.apps_to_include:
                    self.generate_interface_file(model)
        else:
            self.generate_single_interface_file(all_models)
        