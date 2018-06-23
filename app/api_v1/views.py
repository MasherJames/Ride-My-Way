from flask_restful import Resource, reqparse
import json
from ..models import Rides, RideRequest, store
# from flask_jwt_extended import (
#     create_access_token,
#     get_jwt_identity, jwt_required
# )


class RideOffers(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('driver_name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('from', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('to', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('depature', type=str, required=True,
                        help='This field cannot be left blank')
    # @jwt_required

    ''' creating a ride offer '''
# Create a new ride offer

    def post(self):
        # current_user = get_jwt_identity()
        request_data = RideOffers.parser.parse_args()

        driver_name = request_data['driver_name']
        _from = request_data['from']
        to = request_data['to']
        depature = request_data['depature']

        ride_offer = Rides(driver_name, _from, to, depature)

        store['ride_offers'].append(ride_offer)

        return {'message': 'ride offer created succesfully'}, 201

    ''' getting all the ride offers '''
# Get all the ride offers

    def get(self):
        ride_offers = {
            "ride offers": [offer.to_dict() for offer in store['ride_offers']]
        }
        return ride_offers, 200


class SpecificRide(Resource):
    ''' getting a specific ride offer depending on the id passed '''
# Get a specific ride offer depending on the id

    def get(self, rideId):
        ride_offer = {
            'ride_offer': [offer.to_dict() for offer in store['ride_offers']
                           if offer.to_dict()['ride_id'] == rideId]
        }
        return ride_offer, 200


class MakeRideRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('passenger_name', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('from', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('to', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('depature', required=True,
                        help='This field cannot be left blank')
    # Make a request to join a ride

    def post(self, rideId):
        request_data = MakeRideRequest.parser.parse_args()

        passenger_name = request_data['passenger_name']
        _from = request_data['from']
        to = request_data['to']
        depature = request_data['depature']

        ride_request = RideRequest(passenger_name, _from, to, depature)

        store['ride_requests'].append(ride_request)

        return {'message': 'ride offer request created succesfully'}, 201
