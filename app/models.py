from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db,login_manager,admin
from datetime import datetime
from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, pre_load, validate
from flask_weasyprint import HTML,render_pdf

ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    

    # def save_user(self):
    #     db.session.add(self)
    #     db.session.commit()

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        # print(self.password_hash)
        # print(password)
        return check_password_hash(self.password_hash,password)

    # def __init__(self, username, email, password_hash):
    #     self.username = username
    #     self.email = email
    #     self.password_hash = password_hash


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True, validate=validate.Length(1))
    password_hash = fields.String(required=True, validate=validate.Length(1))


class LoginSchema(ma.Schema):
    email = fields.String(required=True, validate=validate.Length(1))
    password_hash = fields.String(required=True, validate=validate.Length(1))



class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(255), unique=True, index=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    asset = db.relationship('Asset', backref='owner', lazy=True)
    trip = db.relationship('Trip', backref='owners', lazy=True)

    # def __init__(self, name, email, phone,asset, date_added):
    #     self.name = name
    #     self.email = email
    #     self.phone = phone
    #     self.asset = asset
    #     self.date_added = date_added
   
  
    def save_owner(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f' {self.name}'


class OwnerSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True, validate=validate.Length(1))
    phone = fields.Integer(required = True)
    asset = fields.String(required=True, validate=validate.Length(1))
    trip = fields.String(required=True, validate=validate.Length(1))
    date_added = fields.String(required=False)


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(10), index=True)
    route = db.relationship("Trip",backref = "asset",lazy = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    
    # def __init__(self,number_plate,route,owner_id):
    #     self.number_plate = number_plate
    #     self.route = route
    #     self.owner_id = owner_id

    @classmethod
    def get_assets(cls):
        assets = Asset.query.order_by('id').all()      
        return assets
    
    @classmethod
    def get_asset(cls,id):
        asset = Asset.query.filter_by(id=id).first()
        return asset 


    def __repr__(self):
        return f' {self.number_plate}'
    
    # def save_asset(self):
    #     db.session.add(self)
    #     db.session.commit()


class AssetSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    number_plate = fields.String(required=True)
    # route = fields.String(required=True, validate=validate.Length(1))
    # owner_id = fields.Integer(required=True)
  


class Staff(UserMixin,db.Model):
    """
    Create an staff table
    """

    __tablename__ = 'staffs'
   
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),index = True)
    phone = db.Column(db.Integer,unique = True)
    email = db.Column(db.String(255),unique = True,index = True)
    date_added = db.Column(db.DateTime,default=datetime.now)
    staff_no = db.Column(db.Integer,unique = True)
    password_hash = db.Column(db.String(255))
    is_admin =db.Column(db.Boolean, default=False)
    
    def save_staff(self):
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
       raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
       self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
       return check_password_hash(self.password_hash,password)

    def __repr__(self):
       return f"Staff('{self.name}', '{self.email}')"


    # def __init__(self,name,phone,email,staff_no, date_added,is_admin):
    #     self.name = name
    #     self.phone = phone
    #     self.email = email
    #     self.staff_no = staff_no
    #     self.date_added = date_added
    #     self.is_admin = is_admin

    def __repr__(self):
        return f' {self.name}'

class StaffSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True, validate=validate.Length(1))
    phone = fields.Integer(required=True)
    staff_no = fields.Integer(required=True)
    date_added = fields.String(required=False)
    # is_admin =db.Column(db.Boolean, default=False)

    
class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.Integer, db.ForeignKey('assets.id'))
    staff_name = db.Column(db.String(255),index = True)
    driver = db.Column(db.String(255),index = True)
    conductor = db.Column(db.String(255),index = True)
    route = db.Column(db.String(255),index = True)
    passengers = db.Column(db.String(255))
    fare = db.Column(db.String(10))
    station = db.Column(db.String(255),index = True)
    time = db.Column(db.DateTime,default=datetime.now)
    owner = db.Column(db.Integer, db.ForeignKey('owners.id'))

    # def __init__(self, number_plate,staff_name, driver, conductor, route, passengers, fare, station, time):
    #     self.number_plate = number_plate
    #     self.staff_name = staff_name
    #     self.driver = driver
    #     self.conductor = conductor
    #     self.route = route
    #     self.passengers = passengers
    #     self.fare = fare
    #     self.station = station
    #     self.time = time

    def __repr__(self):

        return f' {self.route}'

class TripSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    # number_plate = fields.String(required=True)
    staff_name = fields.String(required=True)
    driver = fields.String(required=True)
    conductor = fields.String(required=True)
    route = fields.String(required=True, validate=validate.Length(1))
    passengers = fields.Integer(required=True)
    fare = fields.Integer(required=True)
    station = fields.String(required=True, validate=validate.Length(1))
    time = fields.String(required=False)



def action(name, text, confirmation=None):
    """
        Use this decorator to expose actions that span more than one
        entity (model, file, etc)
        :param name:
            Action name
        :param text:
            Action text.
        :param confirmation:
            Confirmation text. If not provided, action will be executed
            unconditionally.
    """
    def wrap(f):
        f._action = (name, text, confirmation)
        return f
    return wrap

class TheView(ModelView):
    @action('print summary', 'Print Summary', 'Are you sure you want to print these trips summary?')

    def action_recalculate(self, ids):
        #trips = Trips.query.get(ids)
        #trips = Trips.query.all()
        trips = Trip.query.filter(Trip.id.in_(ids)).all()
        name = 'trips'
        ids = ids
        html = render_template('tripsreport.html', ids=ids, name=name, trips=trips)
        owneremail='';
        for singletrip in trips:
            owneremail = singletrip.owners.email ;
            if owneremail != '':
                break
        
        return render_pdf(HTML(string=html))

class Mytools(TheView):
   can_delete = True
   page_size = 50
   column_searchable_list = ['owners.name']

# class Controller(ModelView):
#     def is_accessible(self):
#        if  current_user.is_admin == False:
#            return current_user.is_authenticated
#        else:
#            return abort(403)
#     def not_auth(self):
#        return "you are not authorised"

# admin.add_view(ModelView(User, db.session))        
admin.add_view(ModelView(Owner, db.session))
admin.add_view(ModelView(Staff, db.session))
admin.add_view(ModelView(Asset, db.session))
admin.add_view(Mytools(Trip, db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))



