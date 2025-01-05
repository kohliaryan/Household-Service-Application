from datetime import datetime
from flask import jsonify, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import Professional, Service, db, Request, UserRoles, make_user_professional

api = Api(prefix='/api')

service_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Integer,
    'time_required': fields.Integer,
    'description': fields.String
}

class ServiceAPI(Resource):
    @auth_required('token')
    @marshal_with(service_fields)
    def get(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"msg": "Service not Found"}, 404
        return service
        
    @auth_required('token')
    def delete(self, service_id):
        if current_user.email != "aryan@iit.com":
            return {"msg": "Not Allowed"}, 400
        
        service = Service.query.get(service_id)

        if not service:
            return {"msg": "Service not found"}, 404
        
        db.session.delete(service)
        db.session.commit()
        return {"msg": "Service Deleted Successfully"}, 200

class ServiceListAPI(Resource):
    @auth_required('token')
    @marshal_with(service_fields)
    def get(self):
        services = Service.query.all()
        return services
    
    @auth_required('token')
    def post(self):
        if current_user.email != "aryan@iit.com":
            return {"msg": "Not Allowed"}, 400

        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        time_required = data.get('time_required')

        if not name or not price or not description or not time_required:
            return {'msg': 'Invalid Inputs'}, 400
        
        service = Service(name= name, price= price, time_required= time_required, description= description)

        db.session.add(service)
        db.session.commit()
        return {"msg": "Service Created Succesfully"}, 200
    
professional_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'pincode': fields.String,
    'address': fields.String,
    'experience': fields.String,
    'description': fields.String,
    'service_id': fields.Integer
}

class ProfessionalAPI(Resource):

    @auth_required('token')
    @marshal_with(professional_fields)
    def get(self, prof_id):
        prof = Professional.query.get(prof_id)
        return prof


class ProfessionalListAPI(Resource):

    @auth_required('token')
    @marshal_with(professional_fields)
    def get(self):
        professionals = Professional.query.filter_by(accepted= True).all()
        return professionals

    @auth_required('token')
    def post(self):
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.role_id != 2:
            return {"msg": "Not Allowed"}, 400

        data = request.get_json()
        name = data.get('name')
        pincode = data.get('pincode')
        address = data.get('address')
        experience = data.get('experience')
        description = data.get('description')
        service_id = data.get('service_id')

        if not name or not pincode or not address or not experience or not description or not service_id:
            return {"msg": "Invalid Inputs"}, 400

        service = Service.query.filter_by(id = service_id).first()

        if not service:
            return {"msg" : "Invalid Service"}, 400
        
        make_user_professional(user_id= current_user.id, name=name, pincode=pincode, address=address, experience=experience, description=description, service_id=service_id)

        return {"msg": "Added Succesfully"}
    
api.add_resource(ProfessionalListAPI, "/prof")
api.add_resource(ProfessionalAPI, '/prof/<int:prof_id>')


class AdminAPI(Resource):

    @auth_required('token')
    def put(self, prof_id):
        if current_user.email !="aryan@iit.com":
            return {"msg": "Not Allowed"}, 400

        prof = Professional.query.get(prof_id)
        if prof:
            prof.accepted = True
            db.session.commit()

            return {"msg": "Accepted Succefully"}
        else:
            return {"msg": "Professional not found"}

class AdminListAPI(Resource):
    @auth_required('token')
    @marshal_with(professional_fields)
    def get(self):
        if current_user.email !="aryan@iit.com":
            return {"msg": "Not Allowed"}, 400
        professionals = Professional.query.filter_by(accepted= False).all()
        return professionals

api.add_resource(AdminAPI, '/accept/<int:prof_id>')
api.add_resource(AdminListAPI, '/unprof')

request_fields = {
    'id': fields.Integer,
    'service_id': fields.Integer,
    'customer_id': fields.Integer,
    'professional_id': fields.Integer,
    'date_of_request': fields.DateTime,
    'date_of_completion': fields.DateTime,
    'service_status': fields.String,
    'remarks' : fields.String
}

class RequestAPI(Resource):

    @auth_required('token')
    @marshal_with(request_fields)
    def get(self, service_id):

        request = Request.query.get(service_id)
        if not request:
            return {"msg": "Request not Found"}, 404
        
        if request.customer_id != current_user.id:
            return {"msg": "Not Allowed"}, 400
    
        return request

class RequestListAPI(Resource):
    @auth_required('token')
    @marshal_with(request_fields)
    def get(self):
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.role_id != 3:
            return {"msg": "Not Allowed"}, 400
        requests = Request.query.filter_by(customer_id = current_user.id)
        return requests
    
    @auth_required('token')
    def post(self):
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.role_id != 3:
            return {"msg": "Not Allowed"}, 400
        data = request.get_json()
        service_id = data.get('service_id')
        professional_id = data.get('professional_id')

        if not service_id:
            return {'msg': 'Invalid Inputs'}, 400
        
        service = Service.query.get(service_id)

        if not service:
            return {'msg': 'Service Not Found'}, 404
        
        prof = Professional.query.get(professional_id)

        if not prof or not prof.accepted:
            return {'msg': 'Professional Not Avaiable'}, 404
        
        req = Request(service_id= service_id, customer_id= current_user.id, professional_id= professional_id, date_of_request=datetime.now(), service_status= "requested")

        db.session.add(req)
        db.session.commit()
        return {"msg": "Request Created Succesfully"}, 200

api.add_resource(ServiceAPI, '/services/<int:service_id>')
api.add_resource(ServiceListAPI, '/services')
api.add_resource(RequestAPI, '/request/<int:service_id>')
api.add_resource(RequestListAPI, '/request')