# Django Sales Stat Manager

This is a django project with user authentication system for generating sales statistics in an insightful way. The statistics are generated using `Pandas` module. We will also see the visual representation of the data which will be powered by `Matplotlib` and `Seaborn` modules. We will also have a way to compile the stats into a pdf and view it or download it as we like. The authenticated users can also upload data from the client site as form inputs or as a csv file.

<hr>

## Environment setup

1. Setup a virtual environment first using `virtualenv <your environment name>` and then activate it by running `<env name>\scripts\activate` on Windows or `source bin/activate` on Mac on Linux.

2. Copy the `requirements.txt` in the working directory and run `pip install -r requirements.txt` on your terminal to install all the necessary Python modules.

3. Run `django-admin startproject core .` to create a Django project in the working directory. The `.` creates the project in the root directory of the project.

4. In `core/settings.py` file, add the following settings:

```
STATIC_URL = '/static/' # already existing
STATICFILES_DIRS = [BASE_DIR / 'static'] # new

MEDIA_URL = '/media/' # new
MEDIA_ROOT = BASE_DIR / 'media' # new
```

5. Update `'DIRS': [BASE_DIR / 'templates'],` for the `TEMPLATES` setting. Change the database name if you want, as I changed it as `stats_db.sqlite3`.

6. Run `python manage.py migrate` to initialize the database and then create a super user by running `python manage.py createsuperuser` which will prompt you to provide necessary credentials.

7. Run `python manage.py runserver` to check whether the environment setup has been successful. If everything works fine, you should see the default django template on the browser, add `/admin/` at the end of the URL to visit the admin site.

With this, your environment setup is completed and you are ready to start building all the apps.
