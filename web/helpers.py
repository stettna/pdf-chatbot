"""Helper Functions for chatbot server"""
import os


def allowed_file(filename):
    #validates against allowed file types
    ALLOWED_EXTENSIONS = ['pdf']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_dir(path):
   #creates folder for given path if it does not already exist
   if not os.path.exists(path):
       os.makedirs(path)
   return

