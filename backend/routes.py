from flask import current_app as app, jsonify, render_template,  request, send_file
from flask_security import auth_required, verify_password, hash_password, current_user
from backend.models import User, db
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

        