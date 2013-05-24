# Bhuket

http://bhuket.herokuapp.com/

It makes new S3 buckets with all the proper perms. It is more than that though! It is a soon-to-be-failed attempt to learn some python.

Uses flask and boto, which both seem cool.

## Local Setup

### Init

First, make sure Python, Ruby and Node are installed. This tiny app uses all of them.

Then create your virtual environment:

    easy_install pip # or brew install python
    pip install virtualenvwrapper
    mkvirtualenv --distribute bhuket

Okay, now install all your dependencies:

    pip install -r requirements.txt
    gem install foreman compass bootstrap-sass
    npm install -g coffee-script

### Run

First activate your virtual environment:

    workon bhuket

To start the dev server:

    python app.py

To run tasks:

    python manage.py

## Usage

Hopefully pretty straightforward. It will throw your AWS credentials away at the slightest provocation - it does not want to hold onto those.

## Deployment

- `git remote add heroku git@heroku.com:bhuket.git`
- `git push heroku master`
- Done!

## TODO:

- tests

## Browser Windows I Had Open:

- http://flask.pocoo.org/docs/
- https://devcenter.heroku.com/articles/python
- http://www.artfulcode.net/articles/multi-threading-python/
- https://github.com/holdenmatt/flask-boilerplate
- http://elsdoerfer.name/docs/flask-assets/