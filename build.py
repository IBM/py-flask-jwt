import json


PACKAGE_NAME = 'ibm-flask-jwt'
PACKAGE_VERSION = '0.0.1'


def parse_lockfile():
    dependencies = []
    with open('Pipfile.lock', 'r') as lockfile:
        data = json.loads(lockfile.read())['default']
        dependencies = [f"{key}{value['version']}" for key, value in data.items()]
    return dependencies


setup_config = f'''
from setuptools import setup, find_namespace_packages
setup(
    name = '{PACKAGE_NAME}',
    version = '{PACKAGE_VERSION}',
    description = 'A simple library for securing Flask REST APIs with JWTs using decorators',
    readme = 'README.md',
    package_dir={{'':'lib'}},
    packages = find_namespace_packages(where='lib', exclude=['*test*']),
    install_requires = {parse_lockfile()},
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: Apache 2.0',
        'Operating System :: OS Independent',
    ],
    url = 'https://github.com/IBM/py-flask-jwt'
)
'''


with open('setup.py', 'w') as setup_file:
    setup_file.write(setup_config)
