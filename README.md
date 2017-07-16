The best doctor-patient communication platform ever.

# How to start the project

1. Make sure you have Python(>3.5) installed.

2. Create a new virtual environment for the project:

```bash
$ python3 -m venv venv
```

This will output a folder in the project root named `venv`.

3. Activate the virtual environment!

```bash
$ source venv/bin/activate
```

4. Install all dependent packages.

```bash
(venv)$ pip install -r requirements.txt
```

5. Run database migrations.

```bash
(venv)$ python manage.py migrate
```

6. Create a new superuser if you want to enter into site admin.

```bash
(venv)$ python manage.py createsuperuser
```

Just follow the prompts and do whatever told to do.

7. Run the development server.

```bash
(venv)$ python manage.py runserver
```


# How to initialize elasticsearch

1. Enter the following command to start elasticsearch server at localhost:9200:

```bash
(venv)$ elasticsearch/bin/elasticsearch
```

2. Open another terminal window and run command:

```bash
(venv)$ python manage.py indexdata
```

This will index all data into elasticsearch.


# How to keep pace with the newest project

1. Pull the repository from Github.

```bash
(venv)$ git pull
```

2. Run database migrations.

```bash
(venv)$ python manage.py migrate
```
