## Todo Flask Api
[![Coverage Status](https://coveralls.io/repos/github/andela-ojoloko/Todo-Api/badge.svg?branch=develop)](https://coveralls.io/github/andela-ojoloko/Todo-Api?branch=develop)
[![Build Status](https://travis-ci.org/andela-ojoloko/Todo-Api.svg?branch=develop)](https://travis-ci.org/andela-ojoloko/Todo-Api)
[![Maintainability](https://api.codeclimate.com/v1/badges/959503dbce305a797ea0/maintainability)](https://codeclimate.com/github/andela-ojoloko/Todo-Api/maintainability)

This is Todo todo CRUD Rest API that enables you to create todos and associated todo items. 
The hosted application can be found [here](https://todo-application-api.herokuapp.com/ "herku application link") and API documentaion [here](https://documenter.getpostman.com/view/1865019/RWMLKmFU "postman generated API Docs")

## Tech/framework used 
* [Flask](http://flask.pocoo.org/) A web application microframework for Python.
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) An extension for Flask that adds support for quickly building REST APIs.
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) An extension for Flask that add support for the [ SQLAlchemy](http://www.sqlalchemy.org/) ORM.
* [Marshmallow](https://marshmallow.readthedocs.io/en/3.0/) A simplified object serialization tool.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) An extension that handles SQLAlchemy database migrations for Flask applications. 
* [Flask-Limiter](http://flask-limiter.readthedocs.io/en/stable/) An extension for request rate limiting Flask applications.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
- follow [here](https://docs.python-guide.org/starting/install3/osx/ "python 3 install guide") to install python 3 on OSx
- follow [here](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv "install virtualenv") install vitualenv

### Installing

- clone the repository and navigate into the project directory
``` bash
    git clone https://github.com/andela-ojoloko/Todo-Api.git && cd Todo-Api
```

- create a `python 3` vitrual environment and activate it.
   
    ```bash
    virtualenv -py=python3 venv
    source venv/bin/activate
    ```
- Install the project's requirements
```bash
pip install -r requirements.txt
```

- Copy the content of the `.env_sample` file into a `.env` file. Edit the file to relect your local settings. 

```
cp .env_sample .env
```

- Run database upgrade
```
flask db upgrade
```

- Run the application 

```
flask run
```

#### Making changes to the model

- After making a change to the model, ensure to run the commands below in the order shown to generate a new migration file and apply the migration to the database

```
flask db migrate -m "message indicating change made"
flask db upgrade
```

## Running the Tests
- run the tests with: 
```
pytest -v
```

- generate coverage report with:
```
coverage run -m pytest && coverage report
```


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -m 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



