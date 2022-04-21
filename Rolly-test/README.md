# Mapocracy API

## Description

Mapocracy is an application that allows users to create and vote on polls in their geographic area and represent their votes on a map. Mapocracy API serves as the back-end for Mapocracy. It was created with Python, Flask, SQLAlchemy, and PostgreSQL. 

## Front-End Repository

[Mapocracy](https://github.com/palmswill/mapogracy)

## Live Demo

[Mapocracy](https://mapocracy.herokuapp.com/)

## Features

Users can create polls in which participation is limited to other users within a specified geographic region. Using the interactive map, we can gain insight on the opinions of people living in different areas.

## Setup

1. Open psql and create PostgreSQL database:

```
psql
CREATE DATABASE mapocracy;
```

2. Create a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Create a `.env` file

```
touch .env
```

5. Copy the contents of `.env.sample` and change the database user and password

6. Populate the database with random sample values:

```
python3 tools/populate_db.py
```

7. Run the app:

```
flask run
```

## Contributers
#### Mapocracy-API (back-end)
- [alou64](https://github.com/alou64)
#### Mapocracy (front-end)
- [palmswill](https://github.com/palmswill)
- [eze1er](https://github.com/eze1er)
