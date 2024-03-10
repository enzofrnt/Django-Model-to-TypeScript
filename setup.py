from setuptools import setup, find_packages

setup(
    name='dajngo-models-typescript-types',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
