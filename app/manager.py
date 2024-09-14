from app import database, file_loader

import app.models.data_parsing.model as data_parsing_controller
import app.models.chat_bot.model as chat_bot_controller
import app.models.audio_bot.summarize as audio_bot_controller

from typing import Union 


def extract_data_to_json(file_bytes: bytes, file_name: str) -> dict:
    text = file_loader.load_from_file(file_bytes, file_name)
    text_chuncks = file_loader.split_text(text)
    document_id = database.insert_content(text_chuncks)
    
    response = data_parsing_controller.extract_data_from_documentID(document_id)
        
    return response

def extract_data_to_audio(file_bytes: bytes, file_name: str) -> dict:
    text = file_loader.load_from_audio(file_bytes, file_name)
    text_chuncks = file_loader.split_text(text)
    document_id = database.insert_content_from_string(text_chuncks)
    
    response = audio_bot_controller.summarize(document_id, text)
        
    return response


def search_by_query(query: str, document_id: str = None, user_id: Union[int, str] = 0) -> list[dict]:
    return database.search_by_similar(query, document_id, user_id)


def chat_botQA(question: str, document_id: str, user_id: Union[int, str] = 0) -> dict:
    return chat_bot_controller.chat_bot(question, document_id, user_id)