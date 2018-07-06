from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, jwt_required
)
from ..models import Ride, RideRequest, UserRegister
from ..auth.auth_views import Validation


class RideOffers(Resource):

    @jwt_required
    def get(self):
        ''' Getting all the ride offers '''
        ride = Ride()
        ride_offers = ride.get_all()
        return [ride_offer.to_dict() for ride_offer in ride_offers], 200


class PostRide(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('from', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('to', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('depature', type=str, required=True,
                        help='This field cannot be left blank')

    @jwt_required
    def post(self):
        ''' Creating a ride offer '''

        request_data = PostRide.parser.parse_args()

        driver_name = get_jwt_identity()
        user = UserRegister()
        current_user = user.get_by_username(driver_name)

        if not current_user:
            return {}, 401
        _from = request_data['from']
        to = request_data['to']
        depature = request_data['depature']

        if not Validation().valid_str_fields(_from):
            return {
                'message': 'data should be text, numbers, _, and not empty'
            }, 400

        if not Validation().valid_str_fields(to):
            return {
                'message': 'data should be text, numbers, _, and not empty'
            }, 400

        ride_offer = Ride(current_user, _from, to, depature)
        ride_offer.add()
        return {'message': 'ride offer created succesfully'}, 201


class RideOffer(Resource):

    @jwt_required
    def get(self, rideId):
        ''' Getting a specific ride offer depending on the id passed '''
        ride = Ride()
        ride_offer = ride.get(rideId)
        if not ride_offer:
            return abort(404)
        return ride_offer.to_dict(), 200

    @jwt_required
    def delete(self, rideId):
        ''' Delete a specific ride offer '''
        ride = Ride()
        ride.delete(rideId)

        return {'message': 'ride offer deleted successfully'}, 200


class Request(Resource):

    @jwt_required
    def post(self, rideId):
        '''Make a request to join a specific ride'''
        ride = Ride()
        ride_offer = ride.get(rideId)
        passenger_name = get_jwt_identity()
        user = UserRegister()
        current_user = user.get_by_username(passenger_name)

        if not ride_offer:
            return {'message': 'ride offer does not exist'}, 404

        if not current_user:
            return {'message': 'unauthorized'}, 401

        ride_request = RideRequest(current_user, ride_offer)
        ride_request.add()

        return {'message': 'ride offer request created succesfully'}, 201

    @jwt_required
    def get(self, rideId):
        ''' Fetch requests made for a specific ride '''

        ride = Ride()
        ride_rq = ride.get(rideId)

        if not ride_rq:
            return {'message': 'ride request does not exist'}, 404

        ride_rqst = RideRequest()
        ride_requests = ride_rqst.get_all(rideId)

        return [ride_request.to_dict() for ride_request in ride_requests], 200


class AcceptedRideRequest(Resource):

    @jwt_required
    def put(self, rideId, requestId):
        ''' Accepted ride offer request '''
        ride_rqst = RideRequest()
        ride_rqst.accept(requestId)

        return {'message': 'request accepted'}, 200


class RejectedRideRequest(Resource):

    @jwt_required
    def put(self, rideId, requestId):
        ''' Rejected ride offer request '''
        ride_rqst = RideRequest()
        ride_rqst.reject(requestId)

        return {'message': 'request rejected'}, 200
