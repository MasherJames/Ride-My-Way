from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2


class Model:
    def __init__(self, app=None):
        ''' create a connection to the db '''
        if app is not None:
            self.app = self.init_app(app)
        ''' creating a cursor'''
        self.cursor = self.connect.cursor()

    def init_app(self, app):
        self.connect = psycopg2.connect(
            database=app.config['DATABASE_NAME'],
            user=app.config['DATABASE_USERNAME'],
            password=app.config['DATABASE_PASSWORD'],
            host=app.config['DATABASE_HOST']
        )

    def execute_query(self, query):
        self.cursor.execute(query)

    def save(self):
        self.cursor.commit()

    def close_session(self):
        self.cursor.close()
        self.connect.close()


class Ride(Model):
    """ Ride Model """

    def __init__(self, driver=None, _from=None, to=None, depature=None):
        super().__init__()
        self.driver = driver
        self._from = _from
        self.to = to
        self.depature = depature

    def create_ride_table(self):
        create_ride_table_query = """ CREATE TABLE rides(
            id serial PRIMARY KEY,
            driver VARCHAR(255) NOT NULL,
            _from VARCHAR(50) NOT NULL,
            to VARCHAR(50) NOT NUL,
            depature VARCHAR(50) NOT NUL
        )"""
        self.execute_query(create_ride_table_query)

    def to_dict(self):
        return {
            'driver': self.driver.to_dict(),
            'from':  self._from,
            'to': self.to,
            'depature': self.depature
        }

    def add_ride(self):
        insert_ride_query = (
            """ INSERT INTO rides (driver, _from, to, departure)
             VALUES(%s, %s, %s, %s)""",
            (self.driver, self._from, self.to, self.depature)
        )
        self.execute_query(insert_ride_query)
        self.save()

    def get_ride_by_id(self, ride_id):
        get_ride_by_id_query = (
            """ SELECT * FROM rides WHERE id=(%s)""", (ride_id,)
        )
        data = self.execute_query(get_ride_by_id_query)
        user = data.fetchone()
        return user

    def get_all_rides(self):
        get_all_rides_query = (
            """ SELECT * FROM rides """
        )
        data = self.execute_query(get_all_rides_query)
        rides = data.fetchall()

        all_rides = [ride.to_dict() for ride in rides]
        return all_rides

    def delete_specific_ride(self, ride_id):
        delete_specific_ride_query = (
            """ DELETE FROM rides WHERE ride_id=%s """, (ride_id,)
        )
        self.execute_query(delete_specific_ride_query)
        self.save()


class RideRequest(Model):

    def __init__(self, user=None, ride=None):
        super().__init__(Model)
        self.user = user
        self.ride = ride

    def create_ride_request_table(self):
        create_request_table_query = """ CREATE TABLE ride_requests(
            id serial PRIMARY KEY,
            user VARCHAR(255) NOT NULL,
            ride VARCHAR(255)  NOT NULL
        )"""
        self.execute_query(create_request_table_query)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'ride': self.ride.to_dict()
        }

    def add_ride_request(self):
        insert_ride_request_query = (
            """ INSERT INTO ride_requests (user, ride)
             VALUES(%s, %s)""",
            (self.user, self.ride)
        )
        self.execute_query(insert_ride_request_query)
        self.save()

    def get_all_ride_request(self):
        get_all_ride_request_query = (
            """ SELECT * FROM ride_requests """
        )
        data = self.execute_query(get_all_ride_request_query)
        ride_rqsts = data.fetchall()

        all_ride_requests = [ride_request.to_dict()
                             for ride_request in ride_rqsts]
        return all_ride_requests


class UserRegister(Model):

    def __init__(self, username=None, email=None, password=None, permission=None):
        super().__init__(Model)
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.permission = permission

    def create_user_table(self):
        create_user_query = """ CREATE TABLE users (
             id serial PRIMARY KEY,
             username VARCHAR(20) NOT NULL,
             email VARCHAR(50) NOT NULL,
             password TEXT(16) NOT NULL,
             permission TEXT
        )"""
        self.execute_query(create_user_query)

    def add_user(self):
        insert_user_query = (
            """ INSERT INTO users (username, email, password, permission)
             VALUES(%s, %s, %s, %s)""",
            (self.username,  self.email, self.password_hash, self.permission)
        )
        self.execute_query(insert_user_query)
        self.save()

    def get_user_by_username(self, username):
        get_user_by_name_query = (
            """ SELECT * FROM users WHERE username=(%s)""", (username,)
        )
        data = self.execute_query(get_user_by_name_query)
        user = data.fetchone()
        return user
