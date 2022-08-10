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
    package_dir={{'':'lib'}},
    packages = find_namespace_packages(where='lib', exclude=['*test*']),
    install_requires = {parse_lockfile()}
)
'''


with open('setup.py', 'w') as setup_file:
    setup_file.write(setup_config)
