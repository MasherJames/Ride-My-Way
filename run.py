import os
from app import create_app

app = create_app(os.getenv('MODE') or 'default')


@app.cli.command()
def test():
    import unittest
    all_tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=3).run(all_tests)


@app.cli.command()
def migrate():
    from app.models import Model, Ride, RideRequest, UserRegister
    Model().init_app(app)
    UserRegister().create_table()
    Ride().create_table()
    RideRequest().create_table()


@app.cli.command()
def drop():
    from app.models import Model, Ride, RideRequest, UserRegister
    Model().init_app(app)
    UserRegister().drop('users')
    Ride().drop('rides')
    RideRequest().drop('ride_requests')
