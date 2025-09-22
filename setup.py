from setuptools import setup, find_packages

setup(
    name="drf-keycloak-auth",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "djangorestframework",
        "requests",
    ],
)
