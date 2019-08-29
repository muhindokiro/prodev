from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
from .main.views import (
    UserCategory,OwnerCategory,OwnerById,AssetResource,UserSignIn,AssetById,
    TripResource,TripById,StaffResource)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
# CORS(api)

# @Api.after_request # blueprint can also be app~~
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = '*'
#     return response

# Route

# user registration
api.add_resource(UserCategory, '/user/registration')

# owner list
api.add_resource(OwnerCategory, '/owner')

# single owner
api.add_resource(OwnerById,'/owner/<int:id>')
 
# asset list
api.add_resource(AssetResource, '/asset')

# user login
api.add_resource(UserSignIn,'/user/login')

# # user login
# api.add_resource(UserSignIn,'/user/registration')

# single asset 
api.add_resource(AssetById,'/asset/<int:id>')

# trip list 
api.add_resource(TripResource,'/trip')

# single trip
api.add_resource(TripById,'/trip/<int:t_id>')

# staff list
api.add_resource(StaffResource,'/staff/<int:id>')
