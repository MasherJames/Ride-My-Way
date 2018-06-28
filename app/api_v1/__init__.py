from flask import Blueprint
from .views import RideOffers, RideOffer, Request, FetchedRideRequest, PostRide

api_bp = Blueprint('api', __name__)
