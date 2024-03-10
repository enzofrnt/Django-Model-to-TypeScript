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

To use this utility in your project, you can run the Django management command `django2ts` to generate TypeScript interfaces. Additionally, you can customize the behavior through environment variables such as `TS_APP_TO_INCLUDE`, `TS_PATH`, `TS_SEPERATED_FILES`, and `DJANGO2TS_VERBOSE`. You can also directly use it as CLI command next to your `manage.py` file by using `django2ts` command, with the folowing options:

```
usage: manage.py django2ts [--app APP] [--path PATH] [--separated-files] [--verbose]

And if you want you can also directly use the `ModelToTypeScriptConverter` class in your own code to generate TypeScript interfaces programmatically.

## Installation

`pip install django-model-to-typescript-converter`