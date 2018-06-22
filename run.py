import os
from app import create_app

app = create_app(os.getenv('MODE') or 'default')


@app.cli.command()
def test():
    import unittest
    t = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=1).run(t)
