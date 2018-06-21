import os
from app import create_app
from app.models import store, Rides

app = create_app(os.environ.get('MODE') or 'default')


@app.cli.command()
def test():
    import unittest
    t = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=3).run(t)


# if __name__ == '__main__':
#     app.run()
