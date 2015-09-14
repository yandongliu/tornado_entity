from __future__ import absolute_import

from fabric.api import task, local
from fabric.colors import green, red, magenta

from models import database
from models.session import Session

@task
def hello():
    print green('hi')

@task
def bootstrap_database(environment='development'):
    """Create the database."""

    print green('Creating database')
    database.create()
    print green('Defining schema')
    with open('migrations/schema.sql') as f:
        sql = f.read().replace('\n', '')
    Session.execute(sql)
    Session.commit()

@task
def drop_database(environment='development'):
    """Drop the database."""

    print green('Dropping database')
    database.drop()
