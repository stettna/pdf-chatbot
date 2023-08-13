"""Holds Global data and related functions to be accessed by various files"""

from .chatbot.Convo import Conversation

LLM = "gpt-3.5-turbo"
chunk_size = 500 #size of chunks the data gets split into
overlap = 75 #overlap for each chunk
chat_dict = {} # Dict of Conversation object for each user
data_file_names = {} # Dict of file names each user has loaded in their respective vector stores


def get_convo(id):

    try:
        return chat_dict[id] #returns Conversation object for current user

    except KeyError:
        chat_dict.update({id : Conversation(id, LLM, chunk_size, overlap)})#if user does not have one yet, it gets created and then return
        return chat_dict[id]


def get_file_names(id):

    try:
        return data_file_names[id] #get list of files

    except KeyError:
        data_file_names.update({id : []}) #creates user list
        return data_file_names[id]


def add_file_name(id, file):

    try:
        data_file_names[id].append(file) #Add file name to list
        return

    except KeyError:
        data_file_names.update({id : []}) #Creates list for new user
        data_file_names[id].append(file) #Add file name to list
        return


def clr_file_names(id):
    try:
        data_file_names[id].clear()  # Add file name to list
        return

    except KeyError: #if user has no list just return
        return