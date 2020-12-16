1. Run postgres in Docker (https://hub.docker.com/_/postgres)

```
docker run --name agev_postgres -e POSTGRES_PASSWORD=adminadminadmin -d -p 5432:5432 postgres
```

2. Important resources:
- https://docs.sqlalchemy.org/en/13/ see how a popular ORM is used and how it works
(source code)
- Metaprogramming lectures (9.*) + Python docs
- https://www.python.org/dev/peps/pep-0249/
- https://www.psycopg.org/docs/
- https://www.sphinx-doc.org/en/master/

3. Run unit tests:
```
python -m unittest discover -s test/py2sql/
```

4. Docs were built using this guide https://stackoverflow.com/questions/59903051/sphinxs-autodocs-automodule-having-apparently-no-effect
Sphinx automatically reads the docs
It needs rst files as well as conf.py to be updated and maintained.

5. For demonstration, play with Pycharm database viewing tools (download plugin).

6. Build the project:
```
python setup.py sdist
twine upload dist/*
```
