# Petite URL-Shortner

## Setup
1. Make sure you have `pipenv`, you can install it with `pip install pipenv`
2. Install dependencies from the pipfile with `pipenv install`
3. Enter the virtual shell with `pipenv shell`

## Running Server
The envirnment variable `FLASK_APP` must be set, on unix-shell, you can use
```
export FLASK_APP=index
```
alternatively on windows, you can use
```
set FLASK_APP=index
```
then run the server with
```
flask run
```