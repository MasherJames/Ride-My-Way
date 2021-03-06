import os
from app import create_app
from app.models import Model, UserRegister, Ride, RideRequest

app = create_app(os.getenv('MODE') or 'default')


@app.cli.command()
def test():
    import unittest
    all_tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=3).run(all_tests)


@app.cli.command()
def migrate():
    Model().init_app(app)
    UserRegister().create_table()
    Ride().create_table()
    RideRequest().create_table()


@app.cli.command()
def drop():
    Model().init_app(app)
    UserRegister().drop_table()
    Ride().drop_table()
    RideRequest().drop_table()
