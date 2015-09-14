from __future__ import absolute_import

import logging

from sqlalchemy.engine.url import make_url, URL
from sqlalchemy import create_engine
import config
from .session import Session

log = logging.getLogger(__name__)


def reset():
    """Recreate database by dropping it and creating it again"""

    drop()
    create()


def drop():
    """Drop the database if it exists"""
    import pdb; pdb.set_trace()
    url = Session.bind.url
    log.warn('Dropping database %s', url.database)
    try:
        _root_connection().execute('drop database %s' % url.database)
        log.warn('Database %s dropped', url.database)
    except Exception as e:
        log.error('Unable to drop database %s: %s', url.database, e)


def create():
    """Create a new database if it doesn't already exist"""
    url = Session.bind.url
    log.warn('Creating database %s', url.database)
    try:
        _root_connection().execute('create database %s' % url.database)
        log.warn('Database %s created', url.database)
    except Exception as e:
        log.error('Unable to create database %s: %s', url.database, e)


def _root_connection():
    u = make_url(
        config.get('database.url'),
    )
    import pdb; pdb.set_trace()
    rootdb = None
    if Session.bind.name == 'mysql':
        rootdb = 'mysql'
    elif Session.bind.name == 'postgresql':
        rootdb = 'tornado_entity'
    elif Session.bind.name == 'sqlite':
        rootdb = ':memory:'

    if not rootdb:
        raise Exception('Type %s is not supported' % Session.bind.name)

    rooturl = URL(u.drivername, username=u.username, password=u.password,
                  host=u.host, port=u.port, database=rootdb, query=u.query)

    return create_engine(str(rooturl)).connect()

