import os
import re
import xml.etree.ElementTree as ET

from django.conf import settings
from django.core.management.base import BaseCommand

from django_uml_models.management.constants import ACTION_CHOICES, REGEX_PATTERN


class Command(BaseCommand):
    help = "Manage UML diagrams and Django models."

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, choices=ACTION_CHOICES, help="Action to perform")
        parser.add_argument(
            "app_name", nargs="?", type=str, help="Django app name for specific operations"
        )

    def handle(self, *args, **options):
        action = options["action"]
        app_name = options.get("app_name")

        # Create app folders
        if action == ACTION_CHOICES[0]:
            self.create_app_folders()

        # Create models
        elif action == ACTION_CHOICES[1]:
            if not app_name:
                self.stderr.write(self.style.ERROR("Please provide an app_name."))
                return
            self.create_models(app_name)

        # Compare models
        elif action == ACTION_CHOICES[3]:
            if not app_name:
                self.stderr.write(self.style.ERROR("Please provide an app_name."))
                return
            self.compare_models(app_name)

    def create_app_folders(self):
        """Create UML diagram folders for Django apps."""
        base_path = os.path.join(settings.BASE_DIR, "src", "uml_diagrams")
        os.makedirs(base_path, exist_ok=True)

        for app in settings.INSTALLED_APPS:
            if not app.startswith("django.") and re.match(REGEX_PATTERN, app):
                app_folder = os.path.join(base_path, app)
                os.makedirs(app_folder, exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f"Created folder: {app_folder}"))

    def create_models(self, app_name):
        """Generate models.py based on UML diagram."""
        base_path = os.path.join(settings.BASE_DIR, "src", "uml_diagrams", app_name)
        xml_path = os.path.join(base_path, f"{app_name}.xml")
        models_path = os.path.join(settings.BASE_DIR, app_name, "models.py")

        if not os.path.exists(xml_path):
            self.stderr.write(self.style.ERROR(f"UML diagram not found: {xml_path}"))
            return

        if os.path.exists(models_path) and os.path.getsize(models_path) > 0:
            self.stderr.write(self.style.ERROR(f"models.py is not empty: {models_path}"))
            return

        models_code = self.parse_uml(xml_path)

        with open(models_path, "w") as f:
            f.write(models_code)
        self.stdout.write(self.style.SUCCESS(f"Generated models.py for {app_name}"))

    def compare_models(self, app_name):
        """Compare UML diagram and existing models.py file."""
        base_path = os.path.join(settings.BASE_DIR, "src", "uml_diagrams", app_name)
        xml_path = os.path.join(base_path, f"{app_name}.xml")
        models_path = os.path.join(settings.BASE_DIR, app_name, "models.py")
        log_path = os.path.join(settings.BASE_DIR, "src", "uml_diagrams", "logs", app_name)
        os.makedirs(log_path, exist_ok=True)

        if not os.path.exists(xml_path) or not os.path.exists(models_path):
            self.stderr.write(self.style.ERROR("UML or models.py file missing."))
            return

        with open(models_path) as f:
            models_content = f.read()
        uml_models = self.parse_uml(xml_path)

        diff = self.find_differences(uml_models, models_content)
        log_file = os.path.join(log_path, "diff_log.txt")

        with open(log_file, "w") as f:
            f.write(diff)

        self.stdout.write(self.style.SUCCESS(f"Differences logged at {log_file}"))

    def parse_uml(self, xml_path):
        """Parse UML XML and generate Django models code."""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        model_code = "from django.db import models\n\n"
        models_dict = {}

        for cell in root.findall(".//mxCell"):
            if "value" in cell.attrib and cell.attrib["value"]:
                value = cell.attrib["value"].strip()
                parent = cell.attrib.get("parent", "")

                # Identify table names
                if "shape=table" in cell.attrib.get("style", ""):
                    models_dict[value] = []

                # Identify fields
                elif parent in models_dict:
                    field_parts = value.split()
                    if len(field_parts) < 2:
                        continue

                    field_name = field_parts[0]
                    field_type = field_parts[1].lower()
                    constraints = " ".join(field_parts[2:]).upper()

                    # Map UML types to Django fields
                    type_mapping = {
                        "int": "models.IntegerField()",
                        "char": "models.CharField(max_length=255)",
                        "date": "models.DateField()",
                    }

                    django_field = type_mapping.get(field_type, "models.TextField()")

                    if "NOT NULL" in constraints:
                        django_field = django_field.replace(")", ", null=False)")
                    if "FK" in field_name.upper():
                        ref_table = field_name.split("_")[0].capitalize()
                        django_field = f'models.ForeignKey("{ref_table}", on_delete=models.CASCADE)'

                    models_dict[parent].append(f"    {field_name} = {django_field}")

        for model, fields in models_dict.items():
            model_code += f"class {model}(models.Model):\n"
            if fields:
                model_code += "\n".join(fields) + "\n\n"
            else:
                model_code += "    pass\n\n"

        return model_code

    def find_differences(self, uml_models, models_content):
        """Compare UML-generated models and existing models.py."""
        uml_lines = set(uml_models.split("\n"))
        model_lines = set(models_content.split("\n"))

        added = uml_lines - model_lines
        removed = model_lines - uml_lines

        report = "Differences found:\n"
        if added:
            report += "\nAdded:\n" + "\n".join(added)
        if removed:
            report += "\nRemoved:\n" + "\n".join(removed)
        return report
