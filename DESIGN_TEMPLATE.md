# Django UML CLI - Design Document

Author: Gabryel Nóbrega

## Introduction

### Rationale

The Django UML CLI aims to automate the generation and synchronization of Django models from UML diagrams exported from Draw.io. This tool streamlines model creation, reduces manual errors, and ensures consistency between UML design and Django applications.

### Background

In many Django projects, the database schema is initially designed using UML diagrams. However, translating these designs into Django models is a manual and error-prone process. This tool automates that process, integrating UML-based design directly into Django projects.

### Terminology

- **UML**: Unified Modeling Language, used for visualizing database schemas.
- **Draw.io**: A diagramming tool used to create UML diagrams.
- **Django Models**: Python classes representing database tables in Django.
- **CLI**: Command-line interface used to execute commands in a terminal.

### Non-Goals

- This tool does not validate UML diagrams for correctness beyond syntax validation.
- It does not handle Django migrations automatically; the user must apply migrations manually.

## Proposed Design

### System Architecture

The CLI tool consists of the following components:
- **UML Parser**: Parses XML UML diagrams and extracts table structures.
- **Model Generator**: Converts extracted table structures into Django model definitions.
- **Diff Analyzer**: Compares existing models with UML-generated models and logs differences.
- **File Manager**: Handles file system operations for UML and model files.

### Data Model

Data is stored in UML XML files, which the parser reads to extract table and field definitions. Django models are generated from this structured data.

### Interface/API Definitions

The CLI provides the following commands:
- `createappfolders`: Creates UML storage folders based on Django’s `INSTALLED_APPS`.
- `create-models <app_name>`: Parses UML and generates Django models.
- `compare-models <app_name>`: Compares UML-generated models with existing models and logs differences.

### Business Logic

- **Parsing UML**: Extracts table names, field names, types, and constraints.
- **Generating Models**: Converts extracted information into Django model classes.
- **Comparing Models**: Identifies changes between UML and existing models.

### Migration Strategy

- Users must manually apply Django migrations after model generation using:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## Impact

- **Efficiency**: Reduces the time required to create and update Django models.
- **Consistency**: Ensures that database structures align with the UML design.
- **Maintainability**: Simplifies tracking changes between UML and models.

## Risks

- UML diagrams may be incorrectly formatted, leading to parsing errors.
- If models are modified manually after generation, comparisons may not be accurate.
- The tool does not support complex Django model features like custom managers or proxy models.

## Alternatives

- **Manual Model Creation**: This approach is time-consuming and error-prone.
- **Third-Party Tools**: Some third-party tools exist but may not integrate seamlessly with Django’s ORM.
- **Direct Database Reverse Engineering**: Tools like `inspectdb` can generate models from a database, but this does not enforce UML-based design consistency.

This design ensures a streamlined workflow for UML-based Django model generation and synchronization, optimizing efficiency and consistency in database schema management.
