from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, jwt_required
)
from ..models import Rides, RideRequest, store, get_user_by_username, get_ride_by_id


class RideOffers(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('from', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('to', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('depature', type=str, required=True,
                        help='This field cannot be left blank')

    ''' creating a ride offer '''
    @jwt_required
    def post(self):
        request_data = RideOffers.parser.parse_args()

        driver_name = get_jwt_identity()
        current_user = get_user_by_username(driver_name)
        if not current_user:
            return {}, 401
        _from = request_data['from']
        to = request_data['to']
        depature = request_data['depature']

        ride_offer = Rides(current_user, _from, to, depature)

        store['ride_offers'].append(ride_offer)

        return {'message': 'ride offer created succesfully'}, 201

    ''' getting all the ride offers '''

    @jwt_required
    def get(self):
        ride_offers = {
            "ride offers": [offer.to_dict() for offer in store['ride_offers']]
        }
        return ride_offers, 200


class RideOffer(Resource):
    ''' getting a specific ride offer depending on the id passed '''

    @jwt_required
    def get(self, rideId):
        ride_offer = get_ride_by_id(rideId)
        if not ride_offer:
            return abort(404)
        return ride_offer.to_dict(), 200

    @jwt_required
    def delete(self, rideId):
        item = get_ride_by_id(rideId)
        store['ride_offers'].remove(item)

        return {'message': 'ride offer deleted successfully'}, 200


class Request(Resource):

    '''Make a request to join aride'''
    @jwt_required
    def post(self, rideId):

        ride = get_ride_by_id(rideId)
        passenger_name = get_jwt_identity()
        current_user = get_user_by_username(passenger_name)
        if not current_user:
            return {'message': 'unauthorized'}, 401

        ride_request = RideRequest(current_user, ride)

        store['ride_requests'].append(ride_request)

        return {'message': 'ride offer request created succesfully'}, 201
