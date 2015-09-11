# Beavy

Beavy is a modular (content) community building framework.

## Requirements:

 - Python 3.4+
 - Postgresql 9.4+

## Development setup:

You'll need python3 (3.4+) and npm (2.14+). Start by doing the following:

```
 virtualenv --python python3 venv
 source venv/bin/activate
 pip install -r requirements.txt
 npm install

 # Now edit your app.yml

 # upgrade to latest database
 python manager.py db upgrade heads
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
  npm run hot-dev-server
```

This will start the webpack-dev-server in hot-reload mode on `http://localhost:8080/`


Now point your browser to `http://localhost:8080/` and `http://localhost:8080/webpack-dev-server/` respectively.

---

All changes you now do to either flask backend or webpack frontend files will trigger a hot-reload in the browser. Enjoy!


## Development

A few notes when you want to start developing with beavy.

### Creating new database migrations

_Note_: make sure your database is on the latest version by running `python manager.py db migrate heads`

We use [alembic], wrapped into [flask-migrate] for managing database migrations. The modular concept of beavy makes that a little tricky. In order to keep the database clean on those things you want to have only, we are keeping all migrations that belong to their own modules models inside that model. Which means [alembic runs with multiple heads](http://alembic.readthedocs.org/en/latest/branches.html#running-with-multiple-bases) simultanously. That sounds complicated, but really isn't that much. It just means you need to be careful when creating migrations to place them in the right module with the right dependencies.


If your changes should be part of the main beavy module, create the migration running (within virtualenv):

```
python manager.py db migrate --head=beavy@head
```

This will create a new version in `migrations/versions`. Please review it before applying or committing.

#### Creating migration within a module

In order to ensure consistency between modules and main, you need to specify the current version as a depency for migrations in modules. for that, first find the current revision of the main project:

```
python manager.py db heads | grep beavy\)
=> 242c2fd98af (beavy) (head)
```

In this example `242c2fd98af` is your head revision. Now copy that as a parameter to the migration for your module. In this case we did changes to the 'beavy.likes' modules (you can see all heads with `python manager db heads`). The command looks as follows:

```
python manager.py db migrate --head=beavy.likes@head
```

This should create a new revision in `beavy_modules/likes/migrations` with all changes detected. We now need to add the dependency on main, for that open the newly created file. **And add `depens_on = "242c2fd98af"` in the header as `down_revision`**. And review the rest of the migration.

Now this revision, although only included if the module is activated, will apply those revisions in the proper order. Try it:

```
python manager.py db upgrade heads
```






