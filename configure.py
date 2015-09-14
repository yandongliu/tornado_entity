import logging
import os
import socket

import sqlalchemy

_CONFIGURED = False
logger = logging.getLogger(__name__)


def is_readonly_host():
    return False

def engine_kw(dsn):
    """Get the appropriate engine keywords for a given DSN.

    This is particularly important because there are specific ways to
    do connection pooling for Postgres and MySQL to ensure that load
    balancing works; the out-of-the-box settings in SQLAlchemy are not
    appropriate for either database.
    """
    if dsn.startswith('mysql://'):
        return {'pool_recycle': 60}
    elif dsn.startswith('postgresql'):
        app_name = config.get('application_identifier', 'clay')
        celery_identifier = os.environ.get('CELERY_IDENTIFIER')
        if celery_identifier is not None:
            app_name = '%s:%s' % (app_name, celery_identifier)
        kw = {
            'poolclass': sqlalchemy.pool.NullPool,
            'connect_args': {
                'application_name': '%s@%s.%d' % (
                    app_name, socket.gethostname().split('.')[0], os.getpid())}
            }
        if config.get('sqlalchemy.use_queuepool', False):
            kw['poolclass'] = sqlalchemy.pool.QueuePool
            kw['pool_recycle'] = 60

        if is_readonly_host():
            kw['isolation_level'] = 'AUTOCOMMIT'

        return kw
    else:  # e.g. sqlite
        return {}


def get_dsn(type_='master'):
    """Get a DSN for a specific database type."""
    engine_url = config.get('sqlalchemy.%s.url' % type_)
    if not engine_url and type_ == 'master':
        engine_url = config.get('sqlalchemy.url')
    return engine_url


def get_engine(type_='master'):
    """Get an engine based on its category.

    :param str category: 'master', 'slave', 'batch', etc.
    """
    engine_url = get_dsn(type_)
    if engine_url is None:
        return None
    kw = engine_kw(engine_url)
    engine = sqlalchemy.create_engine(engine_url, **kw)
    engine._type = type_
    return engine


def configure_connections(bind=None):
    """Establish connections to the database.

    :param Engine bind: should be None except for test, gives the
        opportunity to bind against a specific engine.
    """
    from . import session as session_module
    engines = session_module.ENGINES

    global _CONFIGURED
    for type_ in engines.keys():
        engine = bind or get_engine(type_)
        engines[type_] = engine

    # We can't reconfigure existing scoped session, so we need to remove
    # them first.
    session_module.session.remove()
    session_module.session.configure(
        bind=bind or session_module.get_default_bind())

    _CONFIGURED = True
