# OULIPO 
Online application to generate abstract, surreal poetry using the [OULIPO "N+5"](https://en.wikipedia.org/wiki/Oulipo#Constraints) method. See http://oulipo.samwhitehall.com.

## Components
The API uses Django REST Framework. It does two tasks: parts-of-speech tagging/tokenising (using spaCy, in a celery worker) and generating the set of dictionary offsets for each word (this is fast enough to load, so just happens in Django).

The frontend is fairly basic: using Backbone.js and SASS. Grunt is used to concatenate the JS and compile the SASS.

Everything is packaged in Docker, served using nginx and uwsgi.  

## Use
This project uses Docker (hooray!), so the setup should be easy.

* `docker-compose up prod`: production server (nginx/uwsgi).
* `docker-compose up dev`: same as prod server but with volume for live code,
  and DEVELOPMENT environment variable set (slightly different Django settings).
* `docker-compose up tests`: run testbed.


#### Notes
* Include `SECRET_KEY` in `oulipo/oulipo/secrets.py`.
* Include dictionary JSON files in `oulipo/poem/data` (see `scripts/` for how these are generated).
* Run `grunt watch` in `oulipo/frontend` for dev.
