# Item Catalog

This repository contains code for a simple webapp that has a list of items grouped into categories.
I developed this as a part of the Udacity Fullstack Nanodegree programme. The goal is to gain experience
with a web framework (Flask), database development with ORM (PostgreSQL in this case (because it's cool)
used in conjunction with SQLAlchemy) and frontend development and design (HTML, CSS of course) as well.

## Requirements

This project runs inside of the Udacity-provided Fullstack vagrant machine.

To connect to the machine, do the usual `vagrant up && vagrant ssh` from your prompt.

To run the python code, you need (in addition to standard python packages):

1. flask: the web framework of choice here
2. sqlalchemy: the ORM solution of choice
3. sqlalchemy-utils: this package contains some nice utils to help us deal with a few of Postgres' quirks
4. oaut2client: for enabling authentication/authorization related things

The python packages needed are collected in `extra_requirements.txt` and can be installed by running:

```
$ sudo pip install -r extra_requirements.txt
```

In addition to all this, you need to have PostgreSQL installed on your machine. 

If you are a student/reviewer of the Full Stack programme Udacity, all of the above except `sqlalchemy-utils`
should be installed in the Full Stack vagrant machine.

## Running


This program uses Postgres. For initial setup of the database, use:

```
$ python database_setup.py
$ python populate_some_items.py
```

Those commands will set up the database for you and populate it with a few items. To then run the server, use:

```
$ python main.py
```

Once the server is started, go to a browser and access `http://localhost:5001/` to access the DB on your machine.
