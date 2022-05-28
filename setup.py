from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
    with open(file) as f:
        return f.read()

long_description = read_file("README.md")
version = read_file("VERSION")
requirements = read_requirements("requirements.txt")

setup(
    name='airmopss_package',
    version=version,
    license="MIT license",
    author='',
    author_email='',
    url='',
    description='A simple example python package.',
    long_description_content_type="text/x-rst",  # If this causes a warning, upgrade your setuptools package
    long_description=long_description,
    packages=find_packages(exclude=["tests*"]),  # Don't include test directory in binary distribution
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]  # Update these accordingly
)