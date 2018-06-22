from flask import Blueprint
from .views import RideOffers, SpecificRide, MakeRequestRide

api_bp = Blueprint('api', __name__)
