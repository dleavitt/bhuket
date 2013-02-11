# Bhuket

http://bhuket.herokuapp.com/

It makes new S3 buckets with all the proper perms. It is more than that though! It is a soon-to-be-failed attempt to learn some python.

Uses flask and boto, which both seem cool.

## Local Setup

### Init

Install python and pip and virtualenv and ruby and node and npm and all that good stuff. Then run `make init`.

### Run

`make run` - runs the app plus compass and coffeescript change watcher dudes.

Would be nice to have an asset pipeline built into the app, I bet that can be done.

## Usage

Hopefully pretty straightforward. It will throw your AWS credentials away at the slightest provocation - it does not want to hold onto those.

## Deployment

- `git remote add heroku git@heroku.com:bhuket.git`
- `git push heroku master`
- Done!

## TODO:

- force SSL in production (production settings in general)
- tests
- asset situation is a mess

## Browser Windows I Had Open:

- http://flask.pocoo.org/docs/
- https://devcenter.heroku.com/articles/python
- http://www.artfulcode.net/articles/multi-threading-python/
- https://github.com/holdenmatt/flask-boilerplate