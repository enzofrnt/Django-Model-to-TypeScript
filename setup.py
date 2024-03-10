from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dajngo-models-typescript-types',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
    ],
    description='A package to create your Typescript Types/Models from your Django Models.',
    long_description=long_description,
     long_description_content_type="text/markdown",
    author='Enzo_frnt',
    url='https://github.com/enzofrnt/Django-Model-to-TypeScript',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'django2ts=django_model_to_typescript_types:main'
        ],
    },
)
