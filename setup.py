
import os
from setuptools import setup, find_packages

root_dir = os.path.dirname(os.path.abspath(__file__))
req_file = os.path.join(root_dir, 'requirements.txt')
with open(req_file) as f:
    requirements = f.read().splitlines()

setup(
    name='aidbox-sandbox',
    version='0.1',
    description='Aidbox Sandbox',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
