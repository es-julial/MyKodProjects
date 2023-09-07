from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

current_dir = os.path.dirname(__file__)

# engine = create_engine('sqlite:////{}/luckydraw.db'.format(current_dir), conver_unicode=True)
engine = create_engine('sqlite:///{}/luckydraw.db'.format(current_dir), echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
    print('We are connected to database successfully')
