from datetime import datetime
from flask import jsonify, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import Customer, Professional, Service, User, db, Request, UserRoles, make_user_professional

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
    def get(self, service_id):
        prof = Professional.query.filter_by(service_id = service_id, accepted= True).all()
        return prof


class ProfessionalListAPI(Resource):

    @auth_required('token')
    @marshal_with(professional_fields)
    def get(self):
        if current_user.accepted == False:
            return {"msg": "You are Blocked by Admin"}, 403
        professionals = Professional.query.filter_by(accepted= True).all()
        return professionals
    

class AdminListAPI(Resource):
    @auth_required('token')
    @marshal_with(professional_fields)
    def get(self):
        if current_user.email !="aryan@iit.com":
            return {"msg": "Not Allowed"}, 400
        professionals = Professional.query.filter_by(accepted= False).all()
        return professionals

request_fields = {
    'id': fields.Integer,
    'service_id': fields.Integer,
    'customer_id': fields.Integer,
    'professional_id': fields.Integer,
    'date_of_request': fields.DateTime,
    'date_of_completion': fields.DateTime,
    'service_status': fields.String,
    'remarks': fields.String,
    'service_name': fields.String,  
    'professional_name': fields.String ,
    "customer_address": fields.String,
    "customer_name": fields.String 
}

class RequestListAPI(Resource):
    @auth_required('token')
    @marshal_with(request_fields)
    def get(self):
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.role_id == 3:
        # Query all requests for the current user
            requests = Request.query.filter_by(customer_id=current_user.id).all()
        elif role.role_id == 2:
            requests = Request.query.filter_by(professional_id=current_user.id).all()
        else:
            return {"msg": "Not Allowed"}, 400

        result = []
        for req in requests:
            # Get service details
            service = Service.query.filter_by(id=req.service_id).first()
            service_name = service.name if service else None

            # Get professional details
            professional = Professional.query.filter_by(id=req.professional_id).first()
            if not professional:
                return {"msg": "Uncompleted Profile"}, 400
            professional_name = professional.name if professional else None

            # Get customer address details:
            customer = Customer.query.filter_by(id=req.customer_id).first()
            if not customer:
                return {"msg": "Uncompleted Profile"}, 400
            customer_address = customer.address

            # Append request data with service and professional names
            result.append({
                "id": req.id,
                "service_id": req.service_id,
                "customer_id": req.customer_id,
                "professional_id": req.professional_id,
                "date_of_request": req.date_of_request,
                "date_of_completion": req.date_of_completion,
                "service_status": req.service_status,
                "remarks": req.remarks,
                "service_name": service_name,
                "professional_name": professional_name,
                "customer_address": customer_address,
                "customer_name": customer.name
            })

        return result
    @auth_required('token')
    def delete(self):
        # Check if the user has the appropriate role
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.role_id != 2:  # Assuming role_id 2 is authorized to delete requests
            return {"msg": "Not Allowed"}, 400

        # Get the request ID from the JSON payload
        data = request.get_json()
        request_id = data.get('request_id')

        if not request_id:
            return {"msg": "Request ID is required"}, 400

        # Query the request
        req = Request.query.filter_by(id=request_id).first()

        if not req:
            return {"msg": "Request not found"}, 404

        # Delete the request
        db.session.delete(req)
        db.session.commit()

        return {"msg": "Request deleted successfully"}, 200
    
    @auth_required('token')
    def put(self):
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.id == 2:  
            return {"msg": "Not Allowed"}, 400

        # Get the request ID from the JSON payload
        data = request.get_json()
        request_id = data.get('request_id')

        if not request_id:
            return {"msg": "Request ID is required"}, 400

        # Query the request
        req = Request.query.filter_by(id=request_id).first()

        if not req:
            return {"msg": "Request not found"}, 404

        # Ensure the request is in a valid state for accepting
        if req.service_status != "requested":
            return {"msg": "Request cannot be accepted as it is not in the 'requested' state"}, 400

        # Assign the current user (professional) to the request
        req.professional_id = current_user.id
        req.service_status = "assigned"

        db.session.commit()

        return {"msg": "Request accepted successfully", "request_id": req.id}, 200
    
    @auth_required('token')
    def post(self):
        user = User.query.filter_by(id = current_user.id).first()
        if not user.active:
            return {"msg": "Blocked User"}, 403
        role = UserRoles.query.filter_by(user_id=current_user.id).first()
        if role.role_id != 3:
            return {"msg": "Not Allowed"}, 400
        data = request.get_json()
        professional_id = data.get('professional_id')

        prof = Professional.query.get(professional_id)

        if not prof or not prof.accepted:
            return {'msg': 'Professional Not Avaiable'}, 404
        service_id = prof.service_id
        
        req = Request(service_id= service_id, customer_id= current_user.id, professional_id= professional_id, date_of_request=datetime.now(), service_status= "requested")

        db.session.add(req)
        db.session.commit()
        return {"msg": "Request Created Succesfully"}, 200

api.add_resource(ServiceAPI, '/services/<int:service_id>')
api.add_resource(ServiceListAPI, '/services')
api.add_resource(RequestListAPI, '/request') # Used to see all requests to customers and also to Post request and also by professional to delete or accept a particular request
api.add_resource(AdminListAPI, '/unprof') # Used by admin to see all customer
api.add_resource(ProfessionalListAPI, "/prof") # Used to see all accepted professional to customers
api.add_resource(ProfessionalAPI, '/prof/<int:service_id>') # Used to see all accepted professional to customers for that particular service