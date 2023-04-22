from .main import base, create_all
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Entrie(base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    giveaway_id = Column(Integer, ForeignKey("giveaways.id"))

class Giveaway(base):
    __tablename__ = "giveaways"

    id = Column(Integer, primary_key=True)
    prize = Column(String(250))
    ends_in = Column(DateTime)
    desc = Column(String(255))
    channel_id = Column(Integer)
    message_id = Column(Integer)
    host = Column(Integer)
    entries = relationship("Entrie", backref="giveaway", lazy=True)


create_all()


