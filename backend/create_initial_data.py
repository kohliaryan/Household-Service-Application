from flask import current_app as app
from backend.models import (
    add_service,
    db,
    make_user_customer,
    make_user_professional,
    Service
)
from flask_security import SQLAlchemyUserDatastore, hash_password


def seed_database():
    """
    Function to seed the database with default roles and users.
    """
    with app.app_context():
        db.create_all()

        userdatastore: SQLAlchemyUserDatastore = app.security.datastore

        # Create roles if they don't exist
        userdatastore.find_or_create_role(name='Admin', description='root access')
        userdatastore.find_or_create_role(name='Professional', description='Service Professional')
        userdatastore.find_or_create_role(name='Customer', description='An individual who books a service request')

        # Seed Admin user
        if not userdatastore.find_user(email='aryan@iit.com'):
            userdatastore.create_user(email='aryan@iit.com', password=hash_password('pass'), roles=['Admin'])

        # Seed Customer user
        if not userdatastore.find_user(email='user@iit.com'):
            user = userdatastore.create_user(email='user@iit.com', password=hash_password('pass'))
            db.session.commit() 
            make_user_customer(
                user_id=user.id,
                name="Akshit Andotra",
                pincode="184101",
                address="Krishna Colony, Kathua",
            )
        if not Service.query.filter_by(name="Electrical Appliances Reparing Service").first():
            add_service(name="Electrical Appliances Reparing Service", price=1000, time_required=120, description= "Electrical Appliances includes: Air Conditioner, Washing Machine, Fridge and Television")

        # Seed Professional user
        if not userdatastore.find_user(email='prof@iit.com'):
            user = userdatastore.create_user(email='prof@iit.com', password=hash_password('pass'))
            db.session.commit()  # Commit to assign an ID to the user
            make_user_professional(
                user_id=user.id,
                name="Dinesh Sharma",
                pincode="184101",
                address="Shastri Nagar, Kathua",
                experience="3 years",
                description="ITI Diploma Holder in Electrical Engineering",
                service_id=1,
            )

        # Commit changes
        db.session.commit()


# Initialize and seed the database
with app.app_context():
    db.create_all()
    seed_database()
