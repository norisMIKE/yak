import os

from setuptools import find_packages, setup

install_requires = [
    'click',
    'gitpython',
    'jinja2',
    'pathlib2',
    'sqlalchemy',
]


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# Taken from: https://pythonhosted.org/an_example_pypi_project/setuptools.html
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='yak',
    version='0.0.1',
    description=(
        "YAK (Yak Aiohttp devKit) is a tool to help you "
        "kickstart your application and keep your CRUDs DRY."
    ),
    author="panagiks (Kolokotronis Panagiotis)",
    keywords= "aiohttp asyncio framework crud web yak automate",
    license="MIT",
    url = "https://github.com/norisMIKE/yak",
    long_description=read('README.md'),
    classifiers= [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Code Generators",
    ],
    zip_safe=False,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    package_data={
        '': [
            'LICENSE',
            'MANIFEST.in',
            'requirements.txt',
            'src/yak/templates/*',
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yak=yak.run:cli'
        ]
    },
)
