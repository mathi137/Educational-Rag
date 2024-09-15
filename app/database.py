from dotenv import load_dotenv
from typing import Union
from uuid import UUID
import astrapy
import json
import os

load_dotenv() # take environment variables from .env

id_type = Union[str, int]

my_client = astrapy.DataAPIClient(token=os.getenv('ASTRA_DB_APPLICATION_TOKEN'))
my_database = my_client.get_database_by_api_endpoint(api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'))
my_collection = my_database.get_collection(os.getenv('ASTRA_DB_COLLECTION'))


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def insert_content(chuncks, user_id: id_type = 0) -> str:
    document_id = str(astrapy.ids.uuid4())
    
    try:
        my_collection.insert_many([
            {
                'document_id': document_id,
                'user_id': int(user_id),
                'chunk_id': i,
                'content': document.page_content,
                '$vectorize': document.page_content,
            } for i, document in enumerate(chuncks)
        ])
        
    except Exception as e:
        print(f'Exception: {str(e)}')
        
    return document_id


def insert_content_from_string(chuncks: list[str], user_id: id_type = 0) -> str:
    document_id = str(astrapy.ids.uuid4())
    
    try:
        my_collection.insert_many([
            {
                'document_id': document_id,
                'user_id': int(user_id),
                'chunk_id': i,
                'content': text,
                '$vectorize': text,
            } for i, text in enumerate(chuncks)
        ])
        
    except Exception as e:
        print(f'Exception: {str(e)}')
        
    return document_id


def search_by_similar(query: str, document_id: str = None, user_id: id_type = 0, limit: id_type = 20) -> list[dict]:
    filter = [{'user_id': int(user_id)}, {'document_id': document_id}] if document_id else [{'user_id': int(user_id)}]
    
    print('Query:', query)
    
    try:
        cursor = my_collection.find(
            {"$and": filter},
            sort={"$vectorize": query},
            limit=int(limit),
            projection={"$vectorize": True},
            include_similarity=True,
        )
        
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    # Cursor is closed when called
    return list(cursor) 



def search_by_index(index: id_type, document_id: str = None, user_id: id_type = 0) -> list[dict]:
    if document_id:
        filter = [{'user_id': user_id}, {'chunk_id': index},  {'document_id': document_id}]    
    else:
        filter = [{'user_id': user_id}, {'chunk_id': index}] 
    
    try:
        cursor = my_collection.find(
            {"$and": filter},
            limit=1,
        )
        
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    # Cursor is closed when called
    return list(cursor) 