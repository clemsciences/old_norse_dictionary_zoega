"""Config for PyPI."""

import os
import io
from setuptools import find_packages, setup


CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


setup(
    name='zoegas',
    version='1.2.0',
    author='Clément Besnier',
    author_email='clemsciences@aol.com',
    description='Old Norse Zoëga\'s dictionary',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/cltk/old_norse_dictionary_zoega',
    packages=find_packages(),
    include_package_data=True,
    keywords=['nlp', 'old-norse', "philology", "dictionary", "corpus"],
    scripts=[],
    license="License :: OSI Approved :: MIT License",
    zip_safe=True,
    install_requires=['cltk>=0,<1', 'lxml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: XML"
        # "Private :: Do Not Upload"
    ],
    python_requires=">=3.6",
)
