import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Packages required for this module to be executed
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

setuptools.setup(
    name="dsutils", # Replace with your own username
    version="0.0.1",
    author="Greg Strabel",
    author_email="gregory.strabel@gmail.com",
    description="Python Utilities for Data Science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Strabes/dsutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = list_reqs(),
    python_requires='>=3.6',
)