# Item Catalog

This repository contains code for a simple webapp that has a list of items grouped into categories.
I developed this as a part of the Udacity Fullstack Nanodegree programme. The goal is to gain experience
with a web framework (Flask), database development with ORM (PostgreSQL in this case (because it's cool)
used in conjunction with SQLAlchemy) and frontend development and design (HTML, CSS of course) as well.

## Requirements

To run the python code, you need (in addition to standard python packages):

1. flask: the web framework of choice here
2. sqlalchemy: the ORM solution of choice
3. sqlalchemy-utils: this package contains some nice utils to help us deal with a few of Postgres' quirks

The python packages needed are collected in `extra_requirements.txt` and can be installed by running:

```
$ sudo pip install -r extra_requirements.txt
```

In addition to all this, you need to have PostgreSQL installed on your machine. 

If you are a student/reviewer of the Full Stack programme Udacity, all of the above except `sqlalchemy-utils`
should be installed in the Full Stack vagrant machine.