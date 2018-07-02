from flask import Blueprint
from .views import (
    RideOffers, RideOffer, Request,
    PostRide, AcceptedRideRequest, RejectedRideRequest
)

api_bp = Blueprint('api', __name__)
