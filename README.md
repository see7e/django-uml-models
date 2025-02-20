# TODO
- [ ] Add Action Workflows

# **Running the Django UML CLI App**
To test the custom Django management command, follow these steps:


## **1. Ensure Your Django Project is Set Up**
Ensure your Django project is correctly set up with:
- **A valid `settings.py` file** that includes `INSTALLED_APPS`
- **A `manage.py` script** at the root of your Django project
- **Your custom command is placed inside an app directory**

If your project structure is:
```
my_project/
    manage.py
    my_app/
        management/
            commands/
                __init__.py
                mycommand.py
```
Then, `my_app` must be listed inside `INSTALLED_APPS` in `settings.py`.


## **2. Run the CLI Command**
Navigate to your Django project root (where `manage.py` is located) and run:

```bash
python manage.py mycommand --help
```

This should display:

```
usage: manage.py mycommand [-h] {createappfolders,create-models,compare-models} ...
```

This means the command is correctly detected.


## **3. Test Creating UML App Folders**
Run:
```bash
python manage.py mycommand createappfolders
```
Expected Output:
```
Created folder: /path/to/project/src/uml_diagrams/app1
Created folder: /path/to/project/src/uml_diagrams/app2
...
```
Check if the directories exist:
```bash
ls src/uml_diagrams/
```


## **4. Test Generating Models from UML**
- Place a Draw.io UML **exported as XML** inside the `src/uml_diagrams/app_name/` directory.
- Run:
  ```bash
  python manage.py mycommand create-models app_name
  ```
- Expected:
  - `models.py` is generated inside `app_name/`
  - You see:
    ```
    Generated models.py for app_name
    ```
- Verify the file:
  ```bash
  cat app_name/models.py
  ```


## **5. Test Comparing UML and `models.py`**
- Modify `models.py` slightly.
- Run:
  ```bash
  python manage.py mycommand compare-models app_name
  ```
- Expected:
  ```
  Differences logged at /path/to/project/src/uml_diagrams/logs/app_name/diff_log.txt
  ```
- Check the log:
  ```bash
  cat src/uml_diagrams/logs/app_name/diff_log.txt
  ```


## **6. Debugging Issues**
- If the command is **not recognized**, ensure `my_app` is inside `INSTALLED_APPS`.
- If `models.py` **is not generated**, verify the XML file exists.
- If comparisons fail, check the **log file for details**.
