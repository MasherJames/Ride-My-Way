from werkzeug.security import check_password_hash, generate_password_hash

user = {
    'passenger': 1,
    'driver': 2
}


class Rides:
    ride_id = 1

    def __init__(self, driver, _from, to, depature):
        self.driver = driver
        self._from = _from
        self.to = to
        self.depature = depature
        self.id = Rides.ride_id

        Rides.ride_id += 1

    def to_dict(self):
        return {
            'ride_id': self.id,
            'driver': self.driver.to_dict(),
            'from':  self._from,
            'to': self.to,
            'depature': self.depature
        }


class RideRequest:

    ride_request_id = 1

    def __init__(self, user, ride):
        self.user = user
        self.ride = ride
        self.id = RideRequest.ride_request_id

        RideRequest.ride_request_id += 1

    def to_dict(self):
        return {
            'ride_id': self.id,
            'user': self.user.to_dict(),
            'ride': self.ride.to_dict()
        }


class UserRegister:

    user_id = 1

    def __init__(self, username, email, password, permission=user['passenger']):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.id = UserRegister.user_id
        self.permission = permission

        UserRegister.user_id += 1

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'permission': self.permission
        }

    # checks password hash is equal to password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # checks if the user is a driver
    def check_for_driver(self):
        return self.permission == user['driver']


class UserLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }


store = {
    'users': [],
    'ride_offers': [],
    'ride_requests': []
}


def get_user_by_username(username):
    for user in store['users']:
        if user.username == username:
            return user


def get_ride_by_id(ride_id):
    for ride in store['ride_offers']:
        print(ride.ride_id, ride_id)
        if ride.ride_id == ride_id:
            return ride
