import setuptools
from os.path import join

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clivenv",
    version="0.0.4",
    author="duckingod",
    author_email="kingoduck@gmail.com",
    description="Fast access/manage to virtualenv between different python versions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duckingod/clivenv",
    packages=setuptools.find_packages(),
    install_requires=['virtualenv'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console"
    ),
    entry_points={
        'console_scripts': [ 'venv-py=clivenv.venv:main' ]
    },
    scripts=[join('clivenv', 'venv'), join('clivenv', 'venv_pip_recording')],
)

