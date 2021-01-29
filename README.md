# Daedam

## Overview

With the advent of new communication technologies such as YouTube, we are observing a pleasantly surprising trend: the public enjoys and demands deep intellectual discussions. Although it is true that these technologies often tap into more primitive parts of our psychology, they have also revealed existence of the other side, i.e. needs for thoughtful reflection and conversation. Daedam intends to fulfill these largely unmet cognitive needs by helping the audience initiate and organize public intellectual discussions around *their* burning questions in life.

The application serves three types of users:

1. *Audience*, who can create, read, update, and delete `calls`," i.e. requests for questions to be discussed.
2. *Moderator*, who can create, read, update, and delete `offers`, i.e. proposals for discussion events addressing common questions and themes across audience requests.
3. *Administrator*, who can perform all actions.

Note that audience can only read `offers` while a moderator can only read `calls`.

## Deployment

The application has been deployed to Heroku at [https://daedam.herokuapp.com](https://daedam.herokuapp.com).

## API Reference

Documentation of supported endpoints and their details can be found [here](./apidoc.md).

## Local Hosting

You can also host the application locally with the following steps.

### 1. Installing Dependencies

The current project repo uses [`poetry`](https://python-poetry.org/docs/) to manage
dependencies among different Python packages, which is essential to reproducibility.
Following are steps for setting up and getting started:

First, ensure you are using the right version of Python (`3.7.9`). You may want to
use [`pyenv`](https://github.com/pyenv/pyenv) to effectively manage multiple versions
of Python installation. You can then install `poetry`:
```
$ pip install poetry
```

Once you clone the current repo into your local machine, you can go inside the repo and run:
```
$ poetry install
```
to install the right versions of packages for running scripts in the project repo.

To use the new Python configuration that has been installed, you need to run:
```
$ poetry shell
```
which will activate the virtual environment for the project repo.

You can simply type:
```
$ exit
```
to exit from the virtual environment and return to the global (or system) Python installation.

### 2. Setting up the Database

Once the virtual environment is activated, restore the PostgreSQL database to connect and use:
```
$ createdb daedam
$ psql -d daedam -U [username] -a -f daedam.psql
```
where you need to put your system's valid user in `[username]`.

### 3. Configuring Environment Variables

Next, you can set environment variables:
```
$ source setup.sh
```

### 4. Running the Server

Finally, you can launch the backend server:
```
$ flask run
```

For successful launch, make sure that the virtual environment has been activated.

### 5. Testing

You can run tests to ensure the API is working as expected:
```
$ createdb daedam_test
$ psql -d daedam_test -U [username] -a -f daedam.psql
$ export DATABASE_URL=postgres://localhost:5432/daedam_test
$ python tests.py
```
where, again, you need to put your system's valid user in `[username]`.
