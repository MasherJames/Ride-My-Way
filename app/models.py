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
        self.connect.close()


class Rides(Model):

    def __init__(self, driver=None, _from=None, to=None, depature=None):
        super(Model)
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
        res = self.execute_query(get_ride_by_id_query)
        user = res.fetchone()
        return user


class RideRequest(Model):

    def __init__(self, user=None, ride=None):
        super(Model)
        self.user = user
        self.ride = ride

    def create_ride_request_table(self):
        create_request_table_query = """ CREATE TABLE ride_requests(
            id serial PRIMARY KEY,
            user VARCHAR(255) NOT NULL,
            ride VARCHAR(255)  NOT NULL
        )"""
        self.execute_query(create_request_table_query)

    def add_ride_request(self):
        insert_ride_request_query = (
            """ INSERT INTO ride_requests (user, ride)
             VALUES(%s, %s)""",
            (self.user, self.ride)
        )
        self.execute_query(insert_ride_request_query)
        self.save()


class UserRegister(Model):

    def __init__(self, username=None, email=None, password=None, permission=None):
        super.__init__(Model)
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

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_by_username(self, username):
        get_ride_by_name_query = (
            """ SELECT * FROM user WHERE username=(%s)""", (username,)
        )
        res = self.execute_query(get_ride_by_name_query)
        user = res.fetchone()
        return user


def get_user_by_username(self, nams):
    pass


def get_ride_by_id(self, id):
    pass
