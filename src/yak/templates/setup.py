import os

from setuptools import find_packages, setup

install_requires = [
    "aiohttp",
    {% if rest %}"aiohttp_cors",
    {% endif %}"aiohttp_route",
    "{{ database }}[sa]",
]

setup(
    name='{{ project_name }}',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
)
