from setuptools import find_packages, setup

setup(
    name="django-uml-models",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "django",
    ],
    entry_points={
        "console_scripts": [
            "django-uml-models = django_uml_models.management.commands.django_uml:Command.handle",
        ],
    },
    include_package_data=True,
    description="A CLI tool to generate Django models from UML diagrams",
    author="Gabryel Nóbrega",
    author_email="gabryelster@gmail.com",
    url="https://github.com/see7e/django-uml-models",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
)
