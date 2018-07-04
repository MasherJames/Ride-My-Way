import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app
import psycopg2
from config import config


class Model:
    def __init__(self, app=None):
        ''' create a connection to the db '''
        # self.connect = psycopg2.connect(current_app.config.get('DATABASE_URL'))
        self.connect = psycopg2.connect(os.getenv('DATABASE_URL'))
        ''' creating a cursor'''
        self.cursor = self.connect.cursor()

    def init_app(self, app):
        self.connect = psycopg2.connect(app.config.get('DATABASE_URL'))

    def execute_query(self, query):
        self.cursor.execute(query)
        self.save()

    def save(self):
        self.connect.commit()

    def _get_all(self):
        return self.cursor.fetchall()

    def _get_one(self):
        return self.cursor.fetchone()

    def drop(self, name):
        self.cursor.execute(f"""DROP TABLE {name} CASCADE""")
        self.save()

    ''' close connection to the database '''

    def close_session(self):
        self.cursor.close()
        self.connect.close()


class Ride(Model):
    """ Ride Model """

    def __init__(self, driver=None, _from=None, to=None, depature=None):
        super().__init__()
        self.driver = driver
        self._from = _from
        self._to = to
        self.depature = depature
        self.id = None

    def create_table(self):
        create_ride_table_query = """CREATE TABLE IF NOT EXISTS rides(
            id serial PRIMARY KEY,
            driver_id INTEGER NOT NULL,
            _from VARCHAR(50) NOT NULL,
            _to VARCHAR(50) NOT NULL,
            depature CHAR(50) NOT NULL,
            FOREIGN KEY(driver_id) REFERENCES users(id)
         )"""
        self.execute_query(create_ride_table_query)

    ''' drop rides table if it exists '''

    def drop_table(self):
        self.drop('rides')

    ''' add ride into rides table '''

    def add(self):
        self.cursor.execute("""INSERT INTO rides
                     (driver_id, _from, _to, depature) VALUES(%s, %s, %s, %s)
                        """, (self.driver.id, self._from,
                              self._to, self.depature)
                            )
        self.save()

    ''' get a ride by id '''

    def get(self, ride_id):
        self.cursor.execute(
            "SELECT * FROM rides WHERE id=%s", (ride_id,))
        ride = self._get_one()

        if ride:
            return self.map_ride(ride)
        return None

    ''' get all rides '''

    def get_all(self):
        self.cursor.execute("SELECT * FROM rides")
        rides = self._get_all()

        if rides:
            return [self.map_ride(r) for r in rides]
        return None

    ''' delete ride by id '''

    def delete(self, ride_id):
        self.cursor.execute(
            "DELETE FROM rides WHERE id=%s", (ride_id,))
        self.save()

    ''' mapping a ride to a dictionary '''

    def to_dict(self):
        return dict(
            id=self.id,
            driver=self.driver.to_dict(),
            _from=self._from,
            _to=self._to,
            depature=self.depature
        )

    ''' map ride to an object '''

    def map_ride(self, data):
        r = Ride(driver=UserRegister().get_by_id(
            data[1]), _from=data[2], to=data[3], depature=data[4])
        r.id = data[0]
        self = r
        return self


class RideRequest(Model):

    def __init__(self, user=None, ride=None, status='pending'):
        super().__init__(Model)
        self.user = user
        self.ride = ride
        self.status = status

    ''' creating ride_request tables '''

    def create_table(self):
        create_request_table_query = """ CREATE TABLE IF NOT EXISTS ride_requests(
            id serial PRIMARY KEY,
            user_id INTEGER NOT NULL,
            ride_id INTEGER NOT NULL,
            status VARCHAR Not Null,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(ride_id) REFERENCES rides(id)
        )"""
        self.execute_query(create_request_table_query)

    ''' drop table ride_requests if it exists '''

    def drop_table(self):
        self.drop('ride_requests')

    ''' insert a ride request into ride_requests table '''

    def add(self):
        self.cursor.execute(""" INSERT INTO ride_requests (user_id, ride_id, status)
                            VALUES(%s, %s, %s)""",
                            (self.user.id, self.ride.id, self.status)
                            )
        self.save()

    ''' get all ride requests '''

    def get_all(self):
        self.cursor.execute('SELECT * FROM ride_requests')
        ride_rqsts = self._get_all()

        if ride_rqsts:
            return [self.map_request(ride_rqst) for ride_rqst in ride_rqsts]
        return None

    ''' get ride request by id '''

    def get_by_id(self, requestId):
        self.cursor.execute(
            'SELECT * FROM ride_requests WHERE id=%s', (requestId,)
        )
        ride_request = self._get_one()

        if ride_request:
            return self.map_request(ride_request)
        return None

    ''' update a request status to accepted '''

    def accept(self, requestId):
        self.cursor.execute(
            """
            UPDATE ride_requests SET status = (%s) WHERE id=(%s)
             """,
            ('accepted', requestId)
        )
        self.save()

    ''' update a request status to rejected '''

    def reject(self, requestId):
        self.cursor.execute(
            """
            UPDATE ride_requests SET status = (%s) WHERE id=(%s)
             """,
            ('rejected', requestId)
        )
        self.save()

    ''' convert a ride request to a dictionary '''

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.user,
            email=self.ride,
            status=self.status
        )

    ''' map a ride request to an object '''

    def map_request(self, data):
        self.id = data[0]
        self.user = data[1]
        self.ride = data[2]
        self.status = data[3]

        return self


class UserRegister(Model):

    def __init__(self, username=None, email=None, password=None, permission=None):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.permission = permission if permission else 2

    ''' create a users table '''

    def create_table(self):
        create_user_query = """CREATE TABLE IF NOT EXISTS users(
             id serial PRIMARY KEY,
             username VARCHAR(20) NOT NULL UNIQUE,
             email VARCHAR(50) NOT NULL UNIQUE,
             password TEXT NOT NULL,
             permission TEXT
        )"""
        self.execute_query(create_user_query)

    ''' drop users table '''

    def drop_table(self):
        self.drop('users')

    ''' add user into users table '''

    def add(self):
        self.cursor.execute(
            """ INSERT INTO users
                (username, email, password, permission) VALUES(%s, %s, %s, %s)
            """, (self.username,
                  self.email, self.password_hash,
                  self.permission)
        )

        self.save()

    ''' get user by username '''

    def get_by_username(self, username):
        self.cursor.execute(
            'SELECT * FROM users WHERE username=%s', (username,)
        )
        user = self._get_one()

        if user:
            return self.map_user(user)
        return None

    ''' get user by email '''

    def get_by_email(self, email):
        self.cursor.execute(
            'SELECT * FROM users WHERE email=%s', (email,)
        )
        user = self._get_one()

        if user:
            return self.map_user(user)
        return None

    ''' get all users '''

    def get_all(self):
        self.cursor.execute(
            'SELECT * FROM users')
        users = self._get_all()

        if users:
            return [self.map_user(user) for user in users]
        return None

    ''' get user by id '''

    def get_by_id(self, user_id):
        self.cursor.execute(
            'SELECT * FROM users WHERE id=%s', (user_id,)
        )
        user = self._get_one()

        if user:
            return self.map_user(user)
        return None

    ''' map a user to an object '''

    def map_user(self, data):
        self.id = data[0]
        self.username = data[1]
        self.email = data[2]
        self.password_hash = data[3]
        self.permission = data[4]

        return self

    ''' coerce a user into a dictionary '''

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            permission=self.permission
        )
