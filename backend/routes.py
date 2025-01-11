from flask import current_app as app, jsonify, render_template,  request, send_file
from flask_security import auth_required, verify_password, hash_password, current_user
from backend.models import Professional, User, db, make_user_customer, make_user_professional
from datetime import datetime

datastore = app.security.datastore
# cache = app.cache
@app.get('/')
def home():
    return render_template('index.html')

@app.get('/cache')
# @cache.cached(timeout = 5)
def celery():
    return {'time' : str(datetime.now())}

@app.get('/protected')
@auth_required('token')
def protected():
    return '<h1> not Heloi by auth user</h1>'

@auth_required('token')
@app.post('/api/acceptProf/<int:prof_id>')
def acceptProf(prof_id):
    if current_user.email !="aryan@iit.com":
        return {"msg": "Not Allowed"}, 400

    prof = Professional.query.get(prof_id)
    if prof:
        prof.accepted = True
        db.session.commit()

        return {"msg": "Accepted Succefully"}
    else:
        return {"msg": "Professional not found"}
    
@auth_required('token')
@app.delete('/api/deleteProf/<int:prof_id>')
def deleteProf(prof_id):
    # Authorization check
    if current_user.email != "aryan@iit.com":
        return {"msg": "Not Allowed"}, 403

    # Validate prof_id
    if prof_id <= 0:
        return {"msg": "Invalid Professional ID"}, 400

    # Query the Professional record
    prof = Professional.query.get(prof_id)
    if not prof:
        return {"msg": "Professional not found"}, 404

    # Attempt to delete the record
    try:
        db.session.delete(prof)
        db.session.commit()
        return {"msg": "Professional deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"msg": f"An error occurred: {str(e)}"}, 500



@auth_required('token')
@app.post('/api/customerComplete')
def customerComplete():
    data = request.get_json()
    user_id= data.get('user_id')
    name= data.get('name')
    pincode= data.get('pincode')
    address=data.get('address')

    make_user_customer(user_id= user_id, name= name, pincode= pincode, address= address)

    return jsonify({'message' : 'Done'}), 200

@auth_required('token')
@app.post('/api/profComplete')
def profComplete():
    data = request.get_json()
    user_id= data.get('user_id')
    name= data.get('name')
    pincode= data.get('pincode')
    address=data.get('address')
    experience= data.get('experience')
    description= data.get('description')
    service_id= data.get('service_id')

    make_user_professional(user_id= user_id, name= name, pincode= pincode, address= address, experience= experience, description=description, service_id= service_id)

    return jsonify({'message' : 'Done'}), 200


@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg" : "Invalid Inputs"}), 400
    
    user = datastore.find_user(email = email)

    if not user:
        return jsonify({"msg" : "User not exsist"}), 400
    
    if verify_password(password, user.password):
        return jsonify({'token' : user.get_auth_token(), 'email' : user.email, 'role' : user.roles[0].name, 'id' : user.id})
    
    return jsonify({'message' : 'Wrong Password'}), 400

@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or role not in ["Customer", "Professional"]:
        return jsonify({"message": "Invalid Inputs"}), 400
    
    user = datastore.find_user(email = email)

    if user:
        return jsonify({'msg': "Email already registered"}), 400
    
    try:
        if role == "Customer":
            datastore.create_user(email = email, password = hash_password(password), roles = [role], active = True)
        
        else:
            datastore.create_user(email = email, password = hash_password(password), roles = [role], active = True)
        db.session.commit()
        return jsonify({"msg": "User Created Successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"msg": "Error while creating user"}), 400
