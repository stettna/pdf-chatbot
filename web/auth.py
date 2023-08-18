from flask import Blueprint, jsonify, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .__init__ import db
from .helpers import *

auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = './uploads'

@auth.route('/login', methods=['POST'])

def login():

        data = request.get_json()

        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first() #queries user from database

        print("Username:", username, "Password:", password)
        if user: #if found
            if check_password_hash(user.password, password): #matches password
                login_user(user, remember=True)
                response = jsonify({'status': "success", 'message': "user logged in"})
                return response, 200
            else:
                return jsonify({'status': "error", 'message': "incorrect Password"}), 200
        else:
            return jsonify({'status': "error", 'message': "unknown username"}), 200



@auth.route('/logout')
@login_required

def logout():
    try:
        logout_user()
        return jsonify({'status': "success", 'message': "user logged"}), 200
    except:
        return jsonify({'status': "error", 'message': "error occurred in logout"}), 200



@auth.route('/sign-up', methods= ['POST'])
def signup():

    data = request.get_json()
    try:
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
    except KeyError:
        return jsonify({'status': "error", 'message': "missing necessary request field"}), 200

    user = User.query.filter_by(username=username).first() #querys user from database

    if user:
        return jsonify({'status': "error", 'message': "email Already has account"}), 200
    elif len(username) < 3:
        return jsonify({'status': "error", 'message': "username is less than three characters"}), 200
    elif password2 != password2:
        return jsonify({'status': "error", 'message': "passwords do not match"}), 200
    elif len(password1) < 4:
        return jsonify({'status': "error", 'message': "password is less then 4 characters"}), 200
    else:
        #adds user to database and logs them in
        try:
            new_user = User(username=username, password=generate_password_hash( password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            create_dir(UPLOAD_FOLDER + "/" + str(current_user.id))
            f = open(UPLOAD_FOLDER + "/" + str(current_user.id)+ "/uploaded_files.txt", 'w')
            f.close()

            return jsonify({'status': "success", 'message': "user has been sign-up and logged in"}), 200
        except:
            return jsonify({'status': "error", 'message': "error occurred when creating database entry"}), 200



