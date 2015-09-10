# Beavy

Beavy is a modular (content) community building framework.

## Development setup:

You'll need python3 (3.4+) and npm (2.14+). Start by doing the following:

```
 virtualenv --python python3 venv
 source venv/bin/activate
 pip install -r requirements.txt
 npm install
```


## Run in development

You need two terminals open to run the webpack dev server and flask at the same time.

For flask do:

```
  source venv/bin/activate
  flask --app=main --debug run
```

this will serve the flask backend on `http://localhost:5000/`

Then for webpack you do:

```
  ./node_modules/.bin/webpack-dev-server
```

This will start the webpack-dev-server in hot-reload mode on `http://localhost:8080/`


Now point your browser to `http://localhost:8080/` and `http://localhost:8080/webpack-dev-server/` respectively.

---

All changes you now do to either flask backend or webpack frontend files will trigger a hot-reload in the browser. Enjoy!


