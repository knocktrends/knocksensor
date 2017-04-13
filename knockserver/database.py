from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
import os

# Get the database string from config
db_connect_string = config.DATABASE_URI
if config.TESTING:
    db_connect_string = config.TEST_DATABASE_URI


engine = create_engine(db_connect_string, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Initialize SqlAlchemy Base class, see 
# http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import knockserver.models
    Base.metadata.create_all(bind=engine)

if config.TESTING:
    os.remove(config.TEST_DATABASE_URI[10:]) # strip 'sqlite:///'
    init_db()
