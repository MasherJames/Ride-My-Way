from werkzeug.security import check_password_hash, generate_password_hash


# class Permissions:
#     'driver': 1
#     'passenger': 2


class Rides:
    ride_id = 1

    def __init__(self, driver_name, start_from, ends_at, date_time):
        self.driver_name = driver_name
        self.start_from = start_from
        self.ends_at = ends_at
        self.date_time = date_time
        self.id = Rides.ride_id

        Rides.ride_id += 1

    def to_dict(self):
        return {
            'ride_id': self.id,
            'driver_name': self.driver_name,
            'start_from':  self.start_from,
            'ends_at': self.ends_at,
            'date_time': self.date_time
        }


# class User:


store = {
    'users': [],
    'ride_offers': []
}
