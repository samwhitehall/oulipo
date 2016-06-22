# OULIPO 
TODO: about the project

## Setup

Install grunt dependencies and generate JS/SCSS

```
$ cd oulipo/frontend
$ npm install
$ grunt watch
```

## Running server

### Backend

1. [rabbitmq] `rabbitmq-server`
2. [celery]   `cd oulipo && celery -A oulipo worker --loglevel=info`  [:5672]
3. [api]      `cd oulipo && django manage.py runserver`               [:8000]

### Static frontend
4. [grunt]    `cd oulipo/frontend && grunt watch`                     [:]
5. [http]     `cd oulipo/frontend && python -m SimpleHTTPServer 8888` [:8888]
