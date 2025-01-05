from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', backref='bearers', secondary='user_roles')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Professional(db.Model): 
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key= True)
    name = db.Column(db.String)
    pincode = db.Column(db.String)
    address = db.Column(db.String)
    experience = db.Column(db.String)  # Years
    description = db.Column(db.String) 
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)

    service = db.relationship('Service', backref='professional')
    user = db.relationship('User',  backref='professional')

class Customer(db.Model): 
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key= True)
    name = db.Column(db.String)
    pincode = db.Column(db.String)
    address = db.Column(db.String)

    user = db.relationship('User',  backref='customer')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  # in minutes
    description = db.Column(db.String)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Assigned professional
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String, nullable=False, default="requested")  # Options: requested, assigned, closed
    remarks = db.Column(db.String, nullable=True)
    
    # Relationships
    service = db.relationship('Service', backref='requests')
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_requests')
    professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_requests')


def make_user_customer(user_id, name, pincode, address):

    user = User.query.get(user_id)
    if not user:
        raise Exception(f"User with ID {user_id} not found.")

    # Check if Customer role exists
    customer_role = Role.query.filter_by(name="Customer").first()
    if not customer_role:
        raise Exception("Customer role not found. Please seed roles first.")

    # Add Customer role to the user
    if customer_role not in user.roles:
        user.roles.append(customer_role)

    # Create Customer entry if not already present
    if not user.customer:
        customer = Customer(
            id=user.id,
            name=name,
            pincode=pincode,
            address=address
        )
        db.session.add(customer)

    db.session.commit()
    print(f"User ID {user_id} is now a Customer.")

def make_user_professional(user_id, name, pincode, address, experience, description, service_id):

    user = User.query.get(user_id)
    if not user:
        raise Exception(f"User with ID {user_id} not found.")

    # Check if Professional role exists
    professional_role = Role.query.filter_by(name="Professional").first()
    if not professional_role:
        raise Exception("Professional role not found. Please seed roles first.")

    # Add Professional role to the user
    if professional_role not in user.roles:
        user.roles.append(professional_role)

    # Create Professional entry if not already present
    if not user.professional:
        professional = Professional(
            id=user.id,
            name=name,
            pincode=pincode,
            address=address,
            experience=experience,
            description=description,
            service_id=service_id,
            accepted= False
        )
        db.session.add(professional)

    db.session.commit()
    print(f"User ID {user_id} is now a Professional.")


def add_service(name, price, time_required, description):
    """
    Adds a new service to the Service table.

    :param name: Name of the service.
    :param price: Price of the service (integer).
    :param time_required: Time required for the service in minutes.
    :param description: Description of the service.
    :return: The newly created Service object.
    """
    # Check if the service already exists
    existing_service = Service.query.filter_by(name=name).first()
    if existing_service:
        raise Exception(f"Service with name '{name}' already exists.")

    # Create a new service
    new_service = Service(
        name=name,
        price=price,
        time_required=time_required,
        description=description
    )
    db.session.add(new_service)
    db.session.commit()  # Save changes to the database
    return new_service

def add_service_request(service_id, customer_id, professional_id=None, remarks=None):

    # Check if the service and customer exist
    service = Service.query.get(service_id)
    if not service:
        raise Exception(f"Service with ID {service_id} does not exist.")
    
    customer = User.query.get(customer_id)
    if not customer:
        raise Exception(f"Customer with ID {customer_id} does not exist.")

    # If professional ID is provided, check if the professional exists
    if professional_id:
        professional = User.query.get(professional_id)
        if not professional:
            raise Exception(f"Professional with ID {professional_id} does not exist.")

    # Create a new service request
    new_request = Request(
        service_id=service_id,
        customer_id=customer_id,
        professional_id=professional_id,
        service_status="requested",
        remarks=remarks
    )

    db.session.add(new_request)
    db.session.commit()  # Save changes to the database
    return new_request
