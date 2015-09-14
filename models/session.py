from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config

db_user = config.get('database.username')
db_pass = config.get('database.password')
db_name = config.get('database.database')
db_url = config.get('database.url')




postgres_str = create_engine('postgresql://{}:{}@localhost:5432/{}'.format(
    db_user, db_pass, db_name,
))
postgres_str = create_engine(db_url)

Session = scoped_session(sessionmaker(postgres_str))
