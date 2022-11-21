[![Actions Status](https://github.com/rezajkee/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/rezajkee/python-project-52/actions)
[![Linter](https://github.com/rezajkee/python-project-52/actions/workflows/linter.yml/badge.svg?branch=main)](https://github.com/rezajkee/python-project-52/actions/workflows/linter.yml)
[![Tests](https://github.com/rezajkee/python-project-52/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/rezajkee/python-project-52/actions/workflows/test.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/0e671059313f10ee4207/maintainability)](https://codeclimate.com/github/rezajkee/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0e671059313f10ee4207/test_coverage)](https://codeclimate.com/github/rezajkee/python-project-52/test_coverage)
-----------
## Task manager

#### The fourth study project on Hexlet

A web application that allows you to set tasks, change its statuses and 
assign executors. Registration and authentication are required to work with 
the system.

#### App on Railway.app:

https://task-manager-as.up.railway.app/

#### Installation via poetry:

##### Clone repository:
```
git clone https://github.com/rezajkee/python-project-52.git
cd python-project-52
```

##### Create .env file in root directory. It should contain:
```
SECRET_KEY="django-insecure-******"  # 50 characters instead of asterisks
DATABASE_URL=sqlite:///path/to/your/root/db.sqlite3
ROLLBAR_ACCESS_TOKEN="Token from rollbar.com to error tracking"
```

##### Install dependencies:
```
make install
```

##### Apply migrations:
```
make migrate
```

##### Run local server:
```
make runserver
```