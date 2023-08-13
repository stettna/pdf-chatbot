from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from .helpers import *
from .cache import *

views = Blueprint('views', __name__)
UPLOAD_FOLDER = './uploads'


@views.route('/chatroom', methods=['POST'])
def chatroom():
    data = request.get_json()

    user_input = data['user_input']  # gets user input from json request

    convo = get_convo(current_user.id) #finds users "Conversation" object

    result = convo.ask_question(user_input)  #asks a question of the AI

    response = {'response' : result["answer"]} #gets response

    return jsonify(response)


@views.route('/upload-file', methods=['POST'])
@login_required
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'status': "error", 'message': "File not found"}), 200

    file = request.files['file'] #gets file from request

    if file.filename == '':
        return jsonify({'status': "error", 'message': "empty file field"}), 200

    if file and allowed_file(file.filename):
        filename = secure_filename(os.path.normpath(file.filename))  # Normalizes path name
        create_dir(UPLOAD_FOLDER + '/' + str(current_user.id))  # Create directory if not already in existence
        path = os.path.join(UPLOAD_FOLDER + '/' + str(current_user.id) + '/', filename)
        file.save(path)  # Save file to directory
        get_convo(current_user.id).add_pdf_data((r"C:" + os.path.join(UPLOAD_FOLDER + '/' + str(current_user.id) + '/', filename)))  # Add file data to chatbot Database
        add_file_name(current_user.id, filename)  # save filename so a list current files can be displayed
        os.remove(path)  # delete file once stored in  the vector store
        return jsonify({'status': "success", 'message': "file added to database"}), 200

    return jsonify({'status': "error", 'message': "unknown error occurred"}), 200


@views.route('/start-chat', methods=['GET'])
def start_chat():
    get_convo(current_user.id).load_db() #loads vector store data into LLM
    return jsonify({'status': "success", 'message': "chat started"}), 200


@views.route('/clr-data', methods=['GET'])
def clr_data():
    get_convo(current_user.id).clr_database() #clears vector store data
    return jsonify({'status': "success", 'message': "data cleared"}), 200