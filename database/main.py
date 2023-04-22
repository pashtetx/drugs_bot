from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///bot.sqlite")
base = declarative_base()

session = sessionmaker(bind=engine)()


def create_all():
    base.metadata.create_all(engine)

