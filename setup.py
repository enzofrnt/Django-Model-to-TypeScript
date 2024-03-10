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
    description='A package to create your Typescript types/models from your Django models.',
    long_description=long_description,
     long_description_content_type="text/markdown",
    author='Horou and Enzo_frnt',
    url='https://github.com/Horou/djangorestframework-deepserializer',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
