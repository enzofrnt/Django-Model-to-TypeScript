THIS MODULE BEINH IN DEVELOPMENT, IT IS NOT READY FOR USE YET.
THE DOCUMENTATION MAY NOT BE ACCURATE.


# Django Model to TypeScript Converter

This repository contains a utility for converting Django models into TypeScript interfaces, facilitating the development of TypeScript applications that interact with Django backends.


## Key Components

### `modeltotypescriptconverter.py`

This file contains the `ModelToTypeScriptConverter` class responsible for the conversion process. It includes methods for processing Django model fields, generating TypeScript interface files, and managing command-line arguments for customization.

### `apps.py`

Defines the `DjangoModelToTypescriptTypesConfig` class, which configures the application and initiates the conversion process during Django's startup if certain conditions are met (based on environment variables).

### Command `django2ts.py`

Located under `management/commands`, this Django management command allows for manual invocation of the conversion process from the command line or within scripts.

## Usage

### Django app
You can use it as Django app by adding it to your `INSTALLED_APPS` in your `settings.py` file.

```python
INSTALLED_APPS = [
    ...
    'django_model_to_typescript_types',
    ...
]
```

It used environment variables to customize the conversion process. So the following environment variables can be set to customize the conversion process:

`TS_APP_TO_INCLUDE` : The name of the Django app containing the models to be converted. Example : `app1,app2`. If not specified, all apps will be included.
`TS_PATH` : The path to the directory where the TypeScript interfaces will be generated. If not specified, the interfaces will be generated in the root directory of the project.
`TS_EXCLUDE_MODELS` : A list of models to exclude from the conversion process. Example : `app1.model1,app2.model2`. If not specified, all models will be included.
`TS_EXLUDE_FIELDS` : A list of fields to exclude from the conversion process. Example : `app1.model1.field1,app2.model2.field2`. If not specified, no fields will be excluded.
`TS_SEPERATED_FILES` : If set to `True`, each interface will be generated in a separate file. If not specified, all interfaces will be generated in a single file.
`DJANGO2TS_VERBOSE` : If set to `True`, the conversion process will print additional information to the console. If not specified, the process will run silently.

### Django management command

You can also use it as a Django management command by running the following command in your terminal:

```shell
manage.py django2ts [--apps APP] [--path PATH] [--exclude-models EXCLUDE_MODELS] [--exclude-fields EXCLUDE_FIELDS] [--seperated-files] [--verbose]
```

This command will use the environment variables to customize the conversion process, but you can also specify the options directly in the command line to override the environment variables.
Here are the available options:

`--apps` : The name of the Django app containing the models to be converted. Example : `app1,app2`. If not specified, all apps will be included.
`--path` : The path to the directory where the TypeScript interfaces will be generated. If not specified, the interfaces will be generated in the root directory of the project.
`--exclude-models` : A list of models to exclude from the conversion process. Example : `app1.model1,app2.model2`. If not specified, all models will be included.
`--exclude-fields` : A list of fields to exclude from the conversion process. Example : `app1.model1.field1,app2.model2.field2`. If not specified, no fields will be excluded.
`--seperated-files` : If set, each interface will be generated in a separate file. If not specified, all interfaces will be generated in a single file.
`--verbose` : If set, the conversion process will print additional information to the console. If not specified, the process will run silently.

Example :

This example will generate TypeScript interfaces for the models in the `myapp` app, excluding `model1` and `model2` off this app, and placing the interfaces in the `/path/to/output` directory. The `--seperated-files` flag will generate a separate file for each interface, and the `--verbose` flag will print additional information to the console.

```shell
python manage.py django2ts --apps myapp --path /path/to/output --exclude-models myapp.model1,myapp.model2 --seperated-files --verbose
```

You can also directly use it as CLI command next to your `manage.py` file by using `django2ts` command, with the same options as the Django management command.

And if you want you can also directly use the `ModelToTypeScriptConverter` class in your own code to generate TypeScript interfaces programmatically.

## Installation

`pip install dajngo-models-typescript-types`

Note:
For the moment there is no possibiity to extend the converter. If you have any recommendation about how to made adding custom traitements possible for some type of Django model field or if you want to add a new feature to the converter, please open an issue. I will be happy to discuss about it.