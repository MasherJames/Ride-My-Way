from flask import Blueprint

from .auth_views import Signup, Login

auth = Blueprint('auth', __name__)
