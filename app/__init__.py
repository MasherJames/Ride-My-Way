from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import config
from .api_v1.views import (
    RideOffers, RideOffer, Request, PostRide,
    AcceptedRideRequest, RejectedRideRequest
)
from .auth.auth_views import Signup, Login

jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    jwt.init_app(app)

    from .api_v1 import api_bp as api_blueprint
    api = Api(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    api_auth = Api(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")

    # Url Routes
    api_auth.add_resource(Signup, '/signup')
    api_auth.add_resource(Login, '/login')

    api.add_resource(RideOffers, '/rides')
    api.add_resource(PostRide, '/users/rides')
    api.add_resource(Request, '/rides/<int:rideId>/requests')
    api.add_resource(RideOffer, '/rides/<int:rideId>')
    api.add_resource(AcceptedRideRequest,
                     '/users/rides/<rideId>/requests/<requestId>/accept')
    api.add_resource(RejectedRideRequest,
                     '/users/rides/<rideId>/requests/<requestId>/reject')

    return app
