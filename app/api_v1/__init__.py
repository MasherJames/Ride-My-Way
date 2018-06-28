from flask import Blueprint
from .views import RideOffers, RideOffer, Request

api_bp = Blueprint('api', __name__)
