import os
from app import create_app
from app.models import Rides

app = create_app(os.getenv('MODE') or 'default')


@app.cli.command()
def test():
    import unittest
    t = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=3).run(t)
