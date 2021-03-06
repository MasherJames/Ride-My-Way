import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app
import psycopg2


class Model:
    def __init__(self):
        ''' Create a connection to the db '''
        self.connect = psycopg2.connect(current_app.config.get('DATABASE_URL'))
        ''' Creating a cursor'''
        self.cursor = self.connect.cursor()

    def init_app(self, app):
        self.connect = psycopg2.connect(app.config.get('DATABASE_URL'))

    def execute_query(self, query):
        self.cursor.execute(query)
        self.save()

    def save(self):
        ''' Save data to the database '''
        self.connect.commit()

    def _get_all(self):
        ''' Fetch all the rows returned '''
        return self.cursor.fetchall()

    def _get_one(self):
        ''' Fetch the first row returned '''
        return self.cursor.fetchone()

    def drop(self, name):
        ''' Drop tables method'''
        self.cursor.execute(f"""DROP TABLE IF EXISTS {name} CASCADE""")
        self.save()

    def close_session(self):
        ''' Close connection to the database '''
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

    def drop_table(self):
        ''' Drop rides table if it exists '''
        self.drop('rides')
        self.close_session()

    def add(self):
        ''' Add ride into rides table '''
        self.cursor.execute("""INSERT INTO rides
                     (driver_id, _from, _to, depature) VALUES(%s, %s, %s, %s)
                        """, (self.driver.id, self._from,
                              self._to, self.depature)
                            )
        self.save()

    def get(self, ride_id):
        ''' Get a ride by id '''
        self.cursor.execute(
            "SELECT * FROM rides WHERE id=%s", (ride_id,))
        ride = self._get_one()

        if ride:
            return self.map_ride(ride)
        return None

    def get_all(self):
        ''' Get all rides '''
        self.cursor.execute("SELECT * FROM rides")
        rides = self._get_all()

        if rides:
            return [self.map_ride(r) for r in rides]
        return None

    def delete(self, ride_id):
        ''' Delete ride by id '''
        self.cursor.execute(
            "DELETE FROM rides WHERE id=%s", (ride_id,))
        self.save()

    def to_dict(self):
        ''' Mapping a ride to a dictionary '''
        return dict(
            id=self.id,
            driver=self.driver.to_dict(),
            _from=self._from,
            _to=self._to,
            depature=self.depature
        )

    def map_ride(self, data):
        ''' Map ride to an object '''
        ride = Ride(driver=UserRegister().get_by_id(
            data[1]), _from=data[2], to=data[3], depature=data[4])
        ride.id = data[0]
        self = ride
        return self


class RideRequest(Model):

    def __init__(self, user=None, ride=None, status='pending'):
        super().__init__()
        self.user = user
        self.ride = ride
        self.status = status

    def create_table(self):
        ''' Creating ride_request tables '''
        create_request_table_query = """ CREATE TABLE IF NOT EXISTS ride_requests(
            id serial PRIMARY KEY,
            user_id INTEGER NOT NULL,
            ride_id INTEGER NOT NULL,
            status VARCHAR NOT Null,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(ride_id) REFERENCES rides(id)
        )"""
        self.execute_query(create_request_table_query)

    def drop_table(self):
        ''' Drop table ride_requests if it exists '''
        self.drop('ride_requests')
        self.close_session()

    def add(self):
        ''' Insert a ride request into ride_requests table '''
        self.cursor.execute(""" INSERT INTO ride_requests (user_id, ride_id, status)
                            VALUES(%s, %s, %s)""",
                            (self.user.id, self.ride.id, self.status)
                            )
        self.save()

    def get_all(self, ride_Id):
        ''' Get all ride requests in a specific ride'''
        self.cursor.execute(
            'SELECT * FROM ride_requests WHERE ride_id=%s', (ride_Id,))
        ride_rqsts = self._get_all()

        if ride_rqsts:
            requests = []
            for ride_rqst in ride_rqsts:
                r_q = {
                    'id': ride_rqst[0],
                    'user': UserRegister().get_by_id(ride_rqst[1]).to_dict(),
                    'ride': ride_rqst[2],
                    'status': ride_rqst[3]
                }
                requests.append(r_q)
            return requests
        return None

    def get_by_id(self, requestId):
        ''' Get ride request by id '''
        self.cursor.execute(
            'SELECT * FROM ride_requests WHERE id=%s', (requestId,)
        )
        ride_request = self._get_one()

        if ride_request:
            return self.map_request(ride_request)
        return None

    def delete_req(self, requestId):
        ''' Delete ride request by id '''
        self.cursor.execute(
            "DELETE FROM ride_requests WHERE id=%s", (requestId,))
        self.save()

    def accept(self, requestId):
        ''' Update a request status to accepted '''
        self.cursor.execute(
            """
            UPDATE ride_requests SET status = (%s) WHERE id=(%s)
             """,
            ('accepted', requestId)
        )
        self.save()

    def reject(self, requestId):
        ''' Update a request status to rejected '''
        self.cursor.execute(
            """
            UPDATE ride_requests SET status = (%s) WHERE id=(%s)
             """,
            ('rejected', requestId)
        )
        self.save()

    def to_dict(self):
        ''' Convert a ride request to a dictionary '''
        return dict(
            id=self.id,
            user_id=self.user,
            ride_id=self.ride,
            status=self.status
        )

    def map_request(self, data):
        ''' Map a ride request to an object '''

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
        self.permission = permission

    def role_level(self, permission):
        ''' check type of the user by permission value '''
        return self.permission == permission

    def create_table(self):
        ''' Create a users table '''
        create_user_query = """CREATE TABLE IF NOT EXISTS users(
             id serial PRIMARY KEY,
             username VARCHAR(20) NOT NULL UNIQUE,
             email VARCHAR(50) NOT NULL UNIQUE,
             password TEXT NOT NULL,
             permission INTEGER NOT NULL
        )"""
        self.execute_query(create_user_query)

    def drop_table(self):
        ''' Drop users table '''
        self.drop('users')
        self.close_session()

    def add(self):
        ''' Add user into users table '''
        self.cursor.execute(
            """ INSERT INTO users
                (username, email, password, permission) VALUES(%s, %s, %s, %s)
            """, (self.username,
                  self.email, self.password_hash,
                  self.permission)
        )

        self.save()

    def get_by_username(self, username):
        ''' Get user by username '''
        self.cursor.execute(
            'SELECT * FROM users WHERE username=%s', (username,)
        )
        user = self._get_one()

        if user:
            return self.map_user(user)
        return None

    def get_by_email(self, email):
        ''' Get user by email '''
        self.cursor.execute(
            'SELECT * FROM users WHERE email=%s', (email,)
        )
        user = self._get_one()

        if user:
            return self.map_user(user)
        return None

    def get_all(self):
        ''' Get all users '''
        self.cursor.execute(
            'SELECT * FROM users')
        users = self._get_all()

        if users:
            return [self.map_user(user) for user in users]
        return None

    def get_by_id(self, user_id):
        ''' Get user by id '''
        self.cursor.execute(
            'SELECT * FROM users WHERE id=%s', (user_id,)
        )
        user = self._get_one()

        if user:
            return self.map_user(user)
        return None

    def map_user(self, data):
        ''' Map a user to an object '''
        self.id = data[0]
        self.username = data[1]
        self.email = data[2]
        self.password_hash = data[3]
        self.permission = data[4]

        return self

    def to_dict(self):
        ''' Coerce a user into a dictionary '''
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            permission=self.permission
        )
