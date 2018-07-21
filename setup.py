import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# TODO: add a license
setup(
    name='django-json-model-translations',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='Have multiple translations for Django model fields and '
                'load these translations using Django localisation framework.',
    long_description=README,
    url='https://github.com/ana-balica/django-json-model-translations',
    author='Ana Balica',
    author_email='ana.balica@gmail.com',
    install_requires=['Django(>=1.11)'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # TODO: test and update later
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
