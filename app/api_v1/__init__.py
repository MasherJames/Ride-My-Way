from flask import Blueprint
from .views import RideOffers, SpecificRide

api_bp = Blueprint('api', __name__)
