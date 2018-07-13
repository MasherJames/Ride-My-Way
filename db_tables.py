from app.models import UserRegister, Ride, RideRequest


def create_tables():
    ''' creating all tables required for testing'''
    user = UserRegister()
    ride = Ride()
    ride_request = RideRequest()

    user.create_table()
    ride.create_table()
    ride_request.create_table()


def drop_tables():
    ''' dropping all existing tables after testing'''
    user = UserRegister()
    ride = Ride()
    ride_request = RideRequest()

    user.drop_table()
    ride.drop_table()
    ride_request.drop_table()
