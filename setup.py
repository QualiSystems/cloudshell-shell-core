import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cloudshell-shell-core",
    url="https://github.com/QualiSystems/cloudshell-shell-core",
    author="Quali",
    license="Apache 2.0",
    author_email="info@quali.com",
    packages=find_packages(),
    install_requires=required,
    python_requires="~=3.7",
    tests_require=required_for_tests,
    version=version_from_file,
    description=(
        "Core package for all CloudShell Shells. This package contains the basic "
        "driver interfaces and metadata definitions as well as utilities and helpers "
        "created specifically for Shells"
    ),
    long_description=(
        "Core package for all CloudShell Shells. This package contains the basic "
        "driver interfaces and metadata definitions as well as utilities and helpers "
        "created specifically for Shells"
    ),
    include_package_data=True,
    keywords="sandbox cloud cmp cloudshell",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
)
