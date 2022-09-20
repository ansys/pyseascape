"""Project installation script."""

from setuptools import find_namespace_packages, setup

setup(
    name="ansys-seascape",
    version="0.1.0",
    url="https://github.com/pyansys/pyseascape",
    author="ANSYS, Inc.",
    author_email="pyansys.support@ansys.com",
    maintainer="Abhishek Kale",
    maintainer_email="abhishek.kale@ansys.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_file="LICENSE",
    description="A pythonic remotable interface to RedHawkSC and TotemSC",
    long_description=open("README.rst").read(),
    install_requires=["importlib-metadata >=4.0", "requests"],
    python_requires=">=3.7",
    packages=find_namespace_packages(where="src", include="ansys*"),
    package_dir={"": "src"},
)
