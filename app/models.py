from werkzeug.security import check_password_hash, generate_password_hash

user = {
    'passenger': 1,
    'driver': 2
}


class Rides:
    ride_id = 1

    def __init__(self, driver_name, _from, to, depature):
        self.driver_name = driver_name
        self._from = _from
        self.to = to
        self.depature = depature
        self.id = Rides.ride_id

        Rides.ride_id += 1

    def to_dict(self):
        return {
            'ride_id': self.id,
            'driver_name': self.driver_name,
            'from':  self._from,
            'to': self.to,
            'depature': self.depature
        }


class RideRequest:

    ride_request_id = 1

    def __init__(self, passenger_name, _from, to, depature):
        self.passenger_name = passenger_name
        self._from = _from
        self.to = to
        self.depature = depature
        self.id = RideRequest.ride_request_id

        RideRequest.ride_request_id += 1

    def to_dict(self):
        return {
            'ride_id': self.id,
            'passenger_name': self.passenger_name,
            'from':  self._from,
            'to': self.to,
            'depature': self.depature
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
            'password':  self.password_hash,
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
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password
        }


store = {
    'users': [],
    'ride_offers': [],
    'ride_requests': []
}
