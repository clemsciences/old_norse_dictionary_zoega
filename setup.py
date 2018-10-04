"""Config for PyPI."""

from setuptools import find_packages
from setuptools import setup

import oldnorsedictionaryzoega

setup(
    author='Clément Besnier',
    author_email='clemsciences@aol.com',
    description='Old Norse Zoëga\'s dictionary',
    include_package_data=True,
    keywords=['nlp', 'old norse', "philology", "dictionary"],
    license='MIT',
    long_description='',
    name='oldnorsedictionaryzoega',
    # package_data={"": "dictionary.xml"},
    packages=find_packages(),
    url='https://github.com/cltk/old_norse_dictionary_zoega',
    version='1.0.0',
    zip_safe=True, install_requires=['cltk']
    # test_suite='cltk.tests.test_cltk',
)
