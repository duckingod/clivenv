import setuptools
from os.path import join

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cli_venv",
    version="0.0.1",
    author="duckingod",
    author_email="kingoduck@gmail.com",
    description="Fast access/manage to virtualenv between different python versions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duckingod/cli_venv",
    packages=setuptools.find_packages(),
    install_requires=[ 'argparse', 'virtualenv' ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console"
    ),
    scripts=[join('venv', 'venv'), join('venv', 'venv.py'), join('venv', 'venv_pip_recording')],
)

