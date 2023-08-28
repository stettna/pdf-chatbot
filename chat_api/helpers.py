"""Helper Functions for chatbot server"""
import os

def allowed_file(filename):
    'validates file against allowed file types'

    ALLOWED_EXTENSIONS = ['pdf']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_dir(path):
   'creates folder for given path if it does not already exist'

   if not os.path.exists(path):
       os.makedirs(path)
   return


def has_source(name, path):
    'checks if filename has already been entered into the database'

    file1 = open(path, "r")
    names = file1.read()
    file1.close()

    if names.find(name) == -1:
        return False
    else:
        return True


def add_data_source(name, path):
    'appends new source to list of sources'

    f = open(path, "a")  # append mode
    f.write(name + "\n")
    f.close()


def get_source_names(path):
    'gets a list of all sources currently in database'

    file1 = open(path, "r")
    names = file1.read().split('\n')
    file1.close()

    return names[ : len(names)-1]


def clr_file(path):
    'clears file of its contents'

    f = open(path, 'r+')
    f.truncate(0)  #need '0' when using r+
    f.close()
    return