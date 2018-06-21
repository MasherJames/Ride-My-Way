from flask_restful import Resource, reqparse
import json
from ..models import Rides, store
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

    def post(self):
        # current_user = get_jwt_identity()
        request_data = RideOffers.parser.parse_args()

        driver_name = request_data['driver_name']
        start_from = request_data['from']
        ends_at = request_data['to']
        date_time = request_data['depature']

        ride_offer = Rides(driver_name, start_from, ends_at, date_time)

        store['ride_offers'].append(ride_offer)

        return {'message': 'ride offer created succesfully'}, 201

    ''' getting all the ride offers '''

    def get(self):
        ride_offers = {
            "ride offers": [offer.to_dict() for offer in store['ride_offers']]
        }
        return ride_offers, 200


class SpecificRide(Resource):
    ''' getting a specific ride offer depending on the id passed '''

    def get(self, rideId):
        ride_offer = {
            'ride_offer': [offer.to_dict() for offer in store['ride_offers'] if offer.to_dict()['ride_id'] == rideId][0]
        }

        if rideId > len(store['ride_offers']):
            return {'message': 'Ride offer not found'}, 404
        return ride_offer, 200
