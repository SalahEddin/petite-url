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

## Running Tests
While inside pipenv shell, run `pytest` that will scan methods that starts with `test`. 

## Design choices
- Chose not to support port numbers for IPv6 since many browsers don't support themwithout a flag [(ref)](https://support.mozilla.org/en-US/questions/1111992).
- Assumed the web service won't be deployed for scaling at the beginning, that's why the counter range method isn't connecting to a separate service managing each deployment range.