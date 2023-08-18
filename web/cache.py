"""Holds Global dict of each users conversation object as well ass related functions to be accessed by various files"""

from .chatbot.Convo import Conversation

LLM = "gpt-3.5-turbo"
chunk_size = 500 #size of chunks the data gets split into
overlap = 75 #overlap for each chunk
chat_dict = {} # Dict of Conversation object for each user


def get_convo(id):

    try:
        return chat_dict[id] #returns Conversation object for current user

    except KeyError:
        chat_dict.update({id : Conversation(id, LLM, chunk_size, overlap)})#if user does not have one yet, it gets created and then return
        return chat_dict[id]


