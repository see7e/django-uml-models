import os
import shutil

import pytest
from django.core.management import call_command

BASE_PATH = os.path.join("src", "uml_diagrams")
TEST_APP_NAME = "fake_app"


@pytest.fixture(scope="function")
def cleanup():
    """Cleanup generated files after each test."""
    yield
    if os.path.exists(BASE_PATH):
        shutil.rmtree(BASE_PATH)
    if os.path.exists(os.path.join(TEST_APP_NAME, "models.py")):
        os.remove(os.path.join(TEST_APP_NAME, "models.py"))


def test_create_app_folders(cleanup):
    """Test if UML directories are created for apps."""
    call_command("django_uml", "createappfolders")
    assert os.path.exists(BASE_PATH), "UML diagrams folder was not created"


def test_create_models_without_app_name():
    """Ensure the command fails when no app_name is provided."""
    with pytest.raises(SystemExit):
        call_command("django_uml", "create-models")


def test_compare_models_without_app_name():
    """Ensure the command fails when no app_name is provided."""
    with pytest.raises(SystemExit):
        call_command("django_uml", "compare-models")


def test_create_models_no_xml(cleanup):
    """Test if create-models fails when XML is missing."""
    with pytest.raises(SystemExit):
        call_command("django_uml", "create-models", TEST_APP_NAME)


def test_compare_models_no_files(cleanup):
    """Test if compare-models fails when UML or models.py is missing."""
    with pytest.raises(SystemExit):
        call_command("django_uml", "compare-models", TEST_APP_NAME)
