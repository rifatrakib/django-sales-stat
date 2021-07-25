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

<hr>

## Models construction

8. For almost any Django project, the first thing we do is to create an app and add models in the spawned `models.py` file. In our project, we will first create 5 apps, include them in the `settings.INSTALLED_APPS` option, and then create necessary models in each of those apps.

9. Run `python manage.py startapp <App name>` command with `"App name" as customers, products, profiles, reports, sales` to create 5 apps. This will create 5 directories in our project with the corresponding app names.

10. Write some models in the `models.py` files of each app as in the repository. There are some additional files in `profiles` and `sales` app. We have a `signals.py` file in the `profiles` app, `signals.py and utils.py` in the `sales` app.

11. The `signals.py` in `profiles` app contains a function which is called when a new user is created. This function creates a profile for the new user automatically. For that, the `ready` method is overriden in the `apps.py` file local to the app. Then the `__init__.py` file is modified with adding the line `default_app_config = 'profiles.apps.ProfilesConfig'` to it.

12. The `signals.py` in `sales` app contains a function which is called when a new sales record is created. This function calculates the total price for all the items selected automatically. For that, the `ready` method is overriden in the `apps.py` file local to the app. Then the `__init__.py` file is modified with adding the line `default_app_config = 'sales.apps.SalesConfig'` to it.

13. The `utils.py` file in `sales` app contains a utility function called `generate_code`. This function uses the `uuid` module to generate a 12-character transaction ID for our sales records automatically. This is called from the overriden `save` method that we wrote in the `Sale` model.

<hr>

## Generate HTML from Pandas dataframe

14. We will create the necessary links in respective `urls.py` scripts and create some function-based and class-based views in respective `views.py` scripts. In our `Home View`, let's make a database call using Django ORM methods and pass the retrieved queryset values into `Pandas.DataFrame` method. This method converts any list type object in Pandas dataframe.

15. Call the `to_html` method on the dataframe object to generate suitable HTML snippet for the dataframe object. This HTML snippet is generated as `<table>` HTML element which is then passed as context in the render method to populate the template file and a response is created. This response is then viewed on the client browser.

<hr>

## Create png image from bytes stream

16. Matplotlib uses different kinds of backends to create images using the data we provide. For our case, we need to display the charts as png images on the frontend; and Anti-Grain Geometry (AGG) backend is the most suitable for this purpose. The bytes stream will be encoded into `base64` object as png format. This can later be decoded as `utf-8`. This can then safely displayed on the template and rendered on the webpage as normal png image which can be viewed and downloaded as well.

17. For generating graphs and charts using matplotlib and seaborn, and then rendering their bytes stream as png format string, we use two functions called `get_chart` and `get_graph` in our `sales/utils.py` script. The `get_chart` function is called from the `home_view` using necessary parameters, the function then uses the parameters to generate to graph image in the IO stream.

18. The `get_chart` function then calls the `get_image` function which uses the IO stream to capture the image as png file and sent to the template to be viewed on the website.

<hr>

## Generate and store reports

19. Using AJAX calls, send form data to the backend with details to include in a report. Create local `static` directory for `reports` app. Then put `home.js` in `static/reports` directory. This file contains javascript to handle sending AJAX requests and receiving JSON reponse and then puting the data from JSON response on the client browser.

20. Use the `ReportForm` ModelForm inside `reports/forms.py` to take necessary inputs for the report object. Then use the view `create_report_view` to store the form data in the database and return JSON response.

21. Create `reports/utils.py` file to include additional support functions for the app. In this case, create a function `get_report_image` to create a png file from raw binary data stream and return the image url after storing it.
