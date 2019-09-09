from datetime import datetime
from flask import abort, redirect, render_template, request, url_for
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash
# from .. import db,photos
from flask_admin import Admin,BaseView
from flask_login import login_user,login_required,current_user,logout_user

import markdown2
from app import admin, db, login_manager
from flask_cors import cross_origin
from ..models import (User, UserSchema,Asset, AssetSchema, LoginSchema, Owner, OwnerSchema,
                      Staff, StaffSchema, Trip, TripSchema)
from ..utils.tokens import GetUserId, Tokens, login_required
from . import main

tk = Tokens()

owners_schema = OwnerSchema(many=True)
owner_schema = OwnerSchema()
users_schema = UserSchema(many=True)
user_schema = UserSchema()
login_schema = LoginSchema()     
assets_schema = AssetSchema(many=True)
asset_schema = AssetSchema()
trips_schema = TripSchema(many=True)
trip_schema = TripSchema()
staffs_schema = StaffSchema(many=True)
staff_schema = StaffSchema()



#comment

# @main.route('/')
# def index():
#     '''
#     View root page function that returns the index page and its data
#     '''
#     return render_template('index.html')

class MyView(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = True
        super(MyView, self).__init__(*args, **kwargs)
        self.admin = Admin()

# @main.route('/')
# # @login_required
# def admin():
#     return MyView().render('admin/index.html')


@main.route('/user/registration', methods=['POST'])
class UserCategory(Resource):
    '''
    View root page function that returns the index page and its data
    '''
    # @cross_origin()
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = user_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400
        # data  = user_schema.load(json_data)
        # if errors:
        #     return errors, 422
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User with email provided already exists'}, 400
        user = User(
            username=json_data['username'],
            email=json_data['email'],
            password_hash=generate_password_hash(json_data['password_hash'])
            )
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return { "status": 'success', 'data': result }, 201

@main.route('/user/login', methods=['POST'])
class  UserSignIn(Resource):
    def post(self):
        """Method to allow user to login"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = login_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        # data, errors = login_schema.load(json_data)
        # if errors:
        #     return errors, 422
        
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {'message': 'No user exists with that email'}, 400
        if user:
            if user.verify_password(data['password_hash']):
                user_id = user.id
                user_token = tk.generate_token(user_id)
                if not user_token:
                    return {
                    'message':'Token Generation Unsuccessful'
                },401
                return {
                        'message':'User logged in successfully',
                        'user_id': user_id,
                        'token': user_token
                    },200
            return {
                'message':'Invalid logging credentials'
            },400


# @login_required
@main.route('/owner', methods=['GET','POST'])
class OwnerCategory(Resource):
    '''
    View root page function that returns the index page and its data
    '''

    # @login_required
    def get(self):
        owners = Owner.query.all()
        owners = owners_schema.dump(owners)
        return {
            'status': 'success',
            'data': owners
        }, 200

    # @cross_origin()
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = owner_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400
        
        owner = Owner.query.filter_by(email=data['email']).first()
        if owner:
            return {'message': 'User with email provided already exists'}, 400
        owner = Owner(
            name=json_data['name'],
            asset=json_data['asset'],
            email=json_data['email'],
            phone=json_data['phone'],
        )
        db.session.add(owner)
        db.session.commit()
        result = owner_schema.dump(owner)
        return { "status": 'success', 'data': result }, 201

@main.route('/owner/<int:id>', methods=['GET','POST'])
class OwnerById(Resource):
    # @login_required
    def get(self,id):
        owner = Owner.query.filter_by(id=id).first()
        print(owner)
        owners = owner_schema.dump(owner)
        if owners:
            return {
                'status': 'success',
                'data': owners
            }, 200
        return {
            'status': 'No owner found',
        }, 400
        
    # @login_required
    def put(self,id):
        userId = GetOwnerId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = owner_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        owner = Owner.query.filter_by(id=id).first()
        # print(owner)
        if not owner:
            return {'message': 'owner does not exist'}, 400
        owner.name = data['name']
        owner.email=data['email']
        owner.asset=data['asset']
        owner.phone=data['phone']
        # owner.date_added=data['date_added']
        # owner.password_hash=data['password_hash']
        db.session.commit()
        # owners = Owner.query.filter_by(id=id).first()
        result = owner_schema.dump(owner)
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    # @login_required
    def delete(self,id):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = owner_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        owners = Owner.query.filter_by(id=id).first()
        # print(owner)
        if not owners:
            return {'message': 'owner does not exist'}, 400
        owner = Owner.query.filter_by(id=id).delete()
        db.session.commit()

        result = owner_schema.dump(owner)

        return { "status": 'success', 'data': result}, 204
 


@main.route('/asset', methods=['GET','POST'])
class AssetResource(Resource):

    def get(self):
        asset = Asset.query.all()
        assets = assets_schema.dump(asset)
        if assets:
            return {
                'status': 'success',
                'data': assets
            }, 200
        return {
            'status': 'No assets found',
        }, 400
    
    # @login_required
    def post(self):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = asset_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400
       
        asset = Asset.query.filter_by(number_plate=data['number_plate']).first()
        print(asset)
        if asset:
            if asset.route == data['route']:            
                return {'message': 'asset already exists in that location'}, 400
        asset = Asset(
            number_plate=json_data['number_plate'],
            # route=json_data['route'],
            # owner_id = json_data['owner_id']
            )
        db.session.add(asset)
        db.session.commit()
        result = asset_schema.dump(asset)
        return { "status": 'success', 'data': result }, 201
    
@main.route('/asset/<int:id>', methods=['GET','POST'])
class AssetById(Resource):
    # @login_required
    def get(self,id):
        asset = Asset.query.filter_by(id=id).first()
        print(asset)
        assets = asset_schema.dump(asset)
        if assets:
            return {
                'status': 'success',
                'data': assets
            }, 200
        return {
            'status': 'No asset found',
        }, 400
        
    # @login_required
    def put(self,id):
        userId = GetOwnerId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = asset_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        asset = Asset.query.filter_by(id=id).first()
        # print(asset)
        if not asset:
            return {'message': 'asset does not exist'}, 400
        asset.number_plate = data['number_plate']
        asset.route=data['route']
        asset.owner_id=data['owner_id']
        db.session.commit()
        # assets = Asset.query.filter_by(id=id).first()
        result = asset_schema.dump(asset)
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    # @login_required
    def delete(self,id):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = asset_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        assets = Asset.query.filter_by(id=id).first()
        # print(asset)
        if not assets:
            return {'message': 'asset does not exist'}, 400
        asset = Asset.query.filter_by(id=id).delete()
        db.session.commit()

        result = asset_schema.dump(asset)

        return { "status": 'success', 'data': result}, 204

@main.route('/trip', methods=['GET','POST'])
class TripResource(Resource):
    # @login_required
    def get(self):
        trip = Trip.query.all()
        trips = trips_schema.dump(trip)
        if trips:
            return {
                'status': 'success',
                'data': trips
            }, 200
        return {
            'status': 'No trips found',
        }, 400
    
    # @login_required
    def post(self):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = trip_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        trip = Trip.query.filter_by(route=data['route']).first()
        # print(trip)
        if trip:           
            return {'message': 'trip already exists in that asset'}, 400
        trip = Trip(
            # number_plate=json_data['number_plate'],
            route=json_data['route'],
            passengers=json_data['passengers'],
            fare=json_data['fare'],
            station=json_data['station'],
            driver=json_data['driver'],
            staff_name=json_data['staff_name'],
            conductor=json_data['conductor'],
            # time=json_data['time'],
            )
        # print(trip.id)
        # trip.id = id
        db.session.add(trip)
        db.session.commit()
        result = trip_schema.dump(trip)
        return { "status": 'success', 'data': result }, 201

@main.route('/trip/<int:id>', methods=['GET','POST'])
class TripById(Resource):
    # @login_required
    def get(self,id):
        trip = Trip.query.filter_by(id=id).first()
        print(trip)
        trips = trip_schema.dump(trip)
        if trips:
            return {
                'status': 'success',
                'data': trips
            }, 200
        return {
            'status': 'No trip found',
        }, 400
        
    # @login_required
    def put(self,id):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = trip_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400
        
        trip = Trip.query.filter_by(id=id).first()
        # print(asset)
        if not trip:           
            return {'message': 'trip does not exists'}, 400
        # trip.number_plate = data['number_plate']
        trip.route=data['route']
        trip.staff_name=data['staff_name']
        trip.passengers=data['passengers']
        trip.fare=data['fare']
        trip.station=data['station']
        trip.driver=data['driver']
        trip.conductor=data['conductor']
        # trip.time=data['time']
        db.session.commit()

        # assets = Asset.query.filter_by(id=id).first()
        result = trip_schema.dump(trip)
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    # @login_required
    def delete(self,id):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data, errors = trip_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        trip = Trip.query.filter_by(id=id).first()
        # print(asset)
        if not trip:           
            return {'message': 'trip does not exists'}, 400
        trip = Trip.query.filter_by(id=id).delete()
        db.session.commit()

        result = trip_schema.dump(trip).data
        return { "status": 'success', 'data': result}, 204

@main.route('/staff', methods=['GET','POST'])
class StaffResource(Resource):
    # @login_required
    def get(self):
        staff = Staff.query.all()
        staffs = staffs_schema.dump(staff)
        if staffs:
            return {
                'status': 'success',
                'data': staffs
            }, 200
        return {
            'status': 'No staffs found',
        }, 400
    
    # @login_required
    def post(self):
        userId = GetUserId.user_creds(self)
        staff = Staff.query.filter_by(id=userId).first()
        # if staff.is_admin != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = staff_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        staff = Staff.query.filter_by(name=data['name']).first()
        # print(staff)
        if staff:           
            return {'message': 'staff already exists in that restaurant'}, 400
        staff = Staff(
            name=json_data['name'],
            phone=json_data['phone'],
            email=json_data['email'],
            staff_no=json_data['staff_no'],
            # is_admin=json_data['is_admin']
            # date_added=json_data['date_added'],
            )
        # print(staff.id)
        # staff.id = id
        db.session.add(staff)
        db.session.commit()
        result = staff_schema.dump(staff)
        return { "status": 'success', 'data': result }, 201
           
    # @login_required
    def put(self):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input

        try:
            data = staff_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400

        staff = Staff.query.filter_by(id=id).first()
        # print(staff)
        if not staff:           
            return {'message': 'staff does not exists in that restaurant'}, 400
        
        staff.name=data['name']
        staff.phone=data['phone']
        staff.email=data['email']
        staff.staff_no=data['staff_no']
        # staff.date_added=data['date_added']
        # staff.is_admin=data['is_admin']
        # staff.id= id
        db.session.commit()
        # assets = Asset.query.filter_by(id=id).first()
        result = staff_schema.dump(staff)
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    # @login_required
    def delete(self,id):
        userId = GetUserId.user_creds(self)
        owner = Owner.query.filter_by(id=userId).first()
        # if owner.role != 'Admin':
        #     return {
        #         'message': 'User not allowed to perform action'
        #     }, 401
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = staff_schema.load(json_data)
        except ValidationError as e:
            return {'message': e.messages}, 400
        
        staff = Staff.query.filter_by(id=id).first()
        # print(staff)
        if not staff:           
            return {'message': 'staff does not exists in that role'}, 400
        staff = Staff.query.filter_by(id=id).delete()
        db.session.commit()

        result = staff_schema.dump(staff)

        return { "status": 'success', 'data': result}, 204
    