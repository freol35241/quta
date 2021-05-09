import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Parse the requirements-txt file and use for install_requires in pip
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="quta",
    version="0.1.0",
    author="Fredrik Olsson",
    author_email="freol@outlook.com",
    maintainer="Fredrik Olsson",
    maintainer_email="freol@outlook.com",
    description="Thrust allocation using Quadratic programming",
    url="https://github.com/freol35241/quta",
    packages=["quta"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=required,
)
