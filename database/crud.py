from .main import session
from .models import Giveaway, Entrie


def delete_giveaway(giveaway):

    session.delete(giveaway)
    session.commit()

def giveaway_add_user(giveaway, user):
    giveaway.entries.append(user)
    session.add(giveaway)
    session.commit()

def add_giveaway(**kwargs):
    giveaway = Giveaway(**kwargs)
    session.add(giveaway)
    session.commit()

def get_giveaway(id, message_id = 0):


    giveaway = session.query(Giveaway).get(id)

    if not id:
        giveaway = session.query(Giveaway).where(Giveaway.message_id == message_id)

    return giveaway.first()


def get_all_giveaways(limit=0) -> list[Giveaway]:
    giveaways = session.query(Giveaway).all()

    if limit != 0:
        pass

    return giveaways

def create_user(user_id, giveaway):
    user = Entrie(user_id = user_id, giveaway = giveaway)
    session.add(user)
    session.commit()

    return user

def delete_user(user: Entrie):

    session.delete(user)
    session.commit()
