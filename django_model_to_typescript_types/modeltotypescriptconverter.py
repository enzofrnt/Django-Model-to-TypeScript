# https://gist.github.com/emoss08/c87c9864ce2af470dc301ff64e39f857
# https://gist.github.com/guizesilva/474fce56fcd5ab766e65e11e0dbff545

from django.apps import apps
from django.core.wsgi import get_wsgi_application

class ModelToTypeScriptConverter:
    def __init__(self, apps_to_include=["app"]):
        self.apps_to_include = apps_to_include
        self.field_type_mapping = {
            "AutoField": "number",
            "BooleanField": "boolean",
            "CharField": "string",
            "DateField": "Date",
            "DateTimeField": "Date",
            "DecimalField": "number",
            "FloatField": "number",
            "ForeignKey": "number",
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
        # Get the WSGI application
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
        # self.get_wsgi_application()
        all_models = apps.get_models()

        with open("/interfaces.ts", "w") as file:
            print("Generating interfaces.ts")
            for model in all_models:
                if model._meta.app_label not in self.apps_to_include:
                    continue

                file.write(f"export interface {model.__name__}{' {'}\n")

                for field in model._meta.fields:
                    _type = self.field_type_mapping.get(field.get_internal_type(), None)
                    if _type is None:
                        continue

                    if field.choices:
                        _type = self.to_type_union(field)

                    name = self.to_camel_case(field.name)

                    # If the field allows null values we add the ? to the type.
                    if field.null:
                        name += "?"

                    file.write(f"\t{name}: {_type};\n")
                file.write("}\n\n")
