from werkzeug.security import check_password_hash, generate_password_hash


# class Permissions:
#     'driver': 1
#     'passenger': 2


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


# class User:


store = {
    'users': [],
    'ride_offers': [],
    'ride_requests': []
}
