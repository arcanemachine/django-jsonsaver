# jsonSaver

jsonSaver is a free service that provides an easy way for users to store and retrieve arbitrary JSON data.

It is made with Django and Django Rest Framework. You can use either the web client powered by Django, or use the API powered by DRF to manage your JSON stores.

### Use Cases

jsonSaver can be used to:

*   Save user settings and config info for frontend apps without having to setup a backend database,
*   Mock API data during testing,
*   Save random JSON snippets,
*   Do anything else you can think of!

### Setup Guide

To run this project on your own server, it helps if you have a bit of Django knowledge.

To run this project:

*   Create a virtualenv for this project
*   Activate the virtualenv and run `pip install -r requirements.txt`
*   Generate a SECRET_KEY in `django_jsonsaver/keys.py` (Instructions [here](https://tech.serhatteker.com/post/2020-01/django-create-secret-key/)). You can also set a key in `django_jsonsaver/settings.py`, but adding the key to `keys.py` will keep the key out of source control.
*   Run the migrations to set up your database (Set to SQLite by default): `./manage.py migrate`

Most common settings are saved in `django_jsonsaver/settings.py` and `django_jsonsaver/server_config.py`.
