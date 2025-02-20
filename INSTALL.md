# **Install Directly from GitHub**
You can install the package using pip like this:

```bash
pip install git+https://github.com/see7e/django-uml-models.git
```

> After the release (to be made)
> ```bash
> pip install git+https://github.com/see7e/django-uml-models.git@v1.0.0
> ```

## **4. Using `requirements.txt`**
If you want to install the package as a dependency, add this to your `requirements.txt`:

```
git+https://github.com/see7e/django-uml-models.git@main
```

Then install using:

```bash
pip install -r requirements.txt
```

---

## **5. Package Structure Considerations**
Ensure your repository has the correct structure for installation:

```
django-uml-models/
    setup.py
    django_uml_cli/
        __init__.py
        management/
            commands/
                __init__.py
                mycommand.py
    requirements.txt
```

Your `setup.py` should have:

```python
from setuptools import setup, find_packages

setup(
    name="django-uml-models",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["django"],
    entry_points={
        "console_scripts": [
            "django-uml-models = django_uml_cli.management.commands.mycommand:Command.handle",
        ],
    },
    include_package_data=True,
    description="A CLI tool to generate Django models from UML diagrams",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/see7e/django-uml-models",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
```

---

## **6. Verify Installation**
After installation, check if it's available:

```bash
django-uml-models --help
```

Or use it in Django:

```bash
python manage.py mycommand createappfolders
```
