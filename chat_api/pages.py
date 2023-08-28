from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from flask_login import current_user
from .helpers import *
from .cache import *

pages = Blueprint('pages', __name__)
UPLOAD_FOLDER = './uploads'


@pages.route('/chatroom', methods=['POST'])
def chatroom():

    print("Asking question")

    data = request.get_json()

    if 'user_input' not in data:
        return jsonify({'status': "error", 'message': "no user_input field"}), 200
    else:
        user_input = data['user_input']  # gets user input from json request

    try:
        convo = get_convo(current_user.id) #finds users "Conversation" object
    except KeyError:
        return jsonify({'status': "error", 'message': 'error occurred when creating conversation'})

    result = convo.ask_question(user_input)  #asks a question of the AI

    if result is not None:
        response = {'response' : result["answer"], 'status' : "success", 'message' : 'question asked successfully'} #gets response
    else:
        response = {'status': "error", 'message': 'error occurred when retrieving response'}

    return jsonify(response)


@pages.route('/upload-file', methods=['POST'])
def upload_file():

    print("Uploading file")

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'status': "error", 'message': "File not found"}), 200
    else:
        file = request.files['file'] #gets file from request

    if file.filename == '':
        return jsonify({'status': "error", 'message': "empty file field"}), 200

    if allowed_file(file.filename):
        filename = secure_filename(os.path.normpath(file.filename)) # Normalizes path name

        if has_source(filename, UPLOAD_FOLDER + "/" +str(current_user.id) + "/uploaded_files.txt"):
            return jsonify({'status': "error", 'message': "file name already entered into vector store"}), 200

        try:

            create_dir(UPLOAD_FOLDER + '/' + str(current_user.id))  # Create directory if not already in existence
            path = os.path.join(UPLOAD_FOLDER + '/' + str(current_user.id) + '/', filename)
            file.save(path)  # Save file to directory

            get_convo(current_user.id).add_pdf_data((r"C:" + path))  # Add file data to chatbot Database

            add_data_source(filename, UPLOAD_FOLDER + "/" +str(current_user.id) + "/uploaded_files.txt")

            os.remove(path)  # delete file once stored in  the vector store
            return jsonify({'status': "success", 'message': "file added to database"}), 200

        except:
            return jsonify({'status': "error", 'message': "error occurred when adding file to vector store"}), 200

    else:
        return jsonify({'status': "error", 'message': "invalid file type"}), 200


@pages.route('/start-chat', methods=['GET'])
def start_chat():
    print("Starting chat")
    try:
        get_convo(current_user.id).memory.clear()
        get_convo(current_user.id).load_db() #loads vector store data into LLM
        return jsonify({'status': "success", 'message': "chat started"}), 200
    except:
        return jsonify({'status': "error", 'message': "error occurred when starting chat"}), 200


@pages.route('/get-file-list', methods=['GET'])
def get_file_list():
    print("Getting file list")
    try:
        return jsonify({'status': "success", 'message': "chat started", "files" : get_source_names(UPLOAD_FOLDER + "/" +str(current_user.id) + "/uploaded_files.txt")}), 200
    except:
        return jsonify({'status': "error", 'message': "error occurred when starting chat"}), 200


@pages.route('/clr-data', methods=['GET'])
def clr_data():
    print("Clearing data")
    try:
        get_convo(current_user.id).clr_database() #clears vector store data
        clr_file(UPLOAD_FOLDER + "/" +str(current_user.id) + "/uploaded_files.txt")

        return jsonify({'status': "success", 'message': "data cleared"}), 200
    except:
        return jsonify({'status': "error", 'message': "error occurred when clearing data"}), 200


@pages.route('/url-data', methods=['POST'])
def url_data():
    print("loading data")

    data = request.get_json()

    if 'url' not in data:
        return jsonify({'status': "error", 'message': "no url field"}), 200
    else:
        url = data['url']  # gets user input from json request

    if has_source(url, UPLOAD_FOLDER + "/" + str(current_user.id) + "/uploaded_files.txt"):
        return jsonify({'status': "error", 'message': "url already entered into vector store"}), 200

    try:
        get_convo(current_user.id).add_web_data(url) #adds vector store data
        add_data_source(url, UPLOAD_FOLDER + "/" +str(current_user.id) + "/uploaded_files.txt")

        return jsonify({'status': "success", 'message': "data added to vector store"}), 200
    except:
        return jsonify({'status': "error", 'message': "error occurred when accessing url"}), 200
