from pathlib import Path

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

from setuptools import find_packages
from setuptools import setup
from os import path


def read_file(filename):
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, filename), encoding='utf-8') as f:
        return f.read()


def requirements(filename):
    """Parse requirements from requirements.txt."""
    path = str(Path(filename))
    reqs = parse_requirements(path, session=False)
    return [str(req.req) for req in reqs]


setup(
    name='sipay',

    version=read_file('VERSION'),

    description='Python SDK',
    long_description=read_file('README.md'),

    author='Sipay Plus SL',
    author_email='develop@sipay.es',

    url='https://github.com/sipay/python-sdk',
    download_url='https://github.com/sipay/python-sdk',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    python_requires='>=3.4',
    platforms=['linux'],

    packages=['sipay'] + list(map(lambda x: "sipay."+x, find_packages('sipay'))),  # noqa

    install_requires=requirements('requirements.txt'),
    dependency_links=[],

    data_files={},
    include_package_data=True,
    zip_safe=False
)
