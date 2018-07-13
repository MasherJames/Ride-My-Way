from app.models import UserRegister, Ride, RideRequest


def create_tables():
    ''' creating all tables required for testing'''
    UserRegister().create_table()
    Ride().create_table()
    RideRequest().create_table()


def drop_tables():
    ''' dropping all existing tables after testing'''
    UserRegister().drop_table()
    Ride().drop_table()
    RideRequest().drop_table()
