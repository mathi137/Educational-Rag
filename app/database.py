import astrapy
from uuid import UUID

from app.utils import bcolors

from dotenv import load_dotenv
from typing import Union
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
    """
    Insert content into the database.

    This function takes a list of objects and inserts them into the database.
    The objects should have a 'page_content' attribute, which is the text to be inserted.
    The function also takes an optional 'user_id' parameter, which is the ID of the user inserting the content.

    Args:
        chuncks (list): A list of objects to be inserted.
        user_id (id_type, optional): The ID of the user. Defaults to 0.

    Returns:
        str: The ID of the document inserted.
    """
    # Generate a unique document ID
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
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        
    return document_id


def insert_content_from_string(chuncks: list[str], user_id: id_type = 0) -> str:
    """
    Insert content into the database from a list of strings.

    Args:
        chuncks (list[str]): A list of strings to be inserted.
        user_id (id_type, optional): The ID of the user. Defaults to 0.

    Returns:
        str: The ID of the document inserted.
    """
    document_id = str(astrapy.ids.uuid4())
    
    # Insert the content into the database
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
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        
    return document_id


def search_by_similar(query: str, document_id: str = None, user_id: id_type = 0, limit: id_type = 10) -> list[dict]:
    """
    Search for similar chunks in the database.

    Args:
        query (str): The query to search for.
        document_id (str, optional): The document ID to search in. Defaults to None.
        user_id (id_type, optional): The user ID to search for. Defaults to 0.
        limit (id_type, optional): The maximum number of results to return. Defaults to 10.

    Returns:
        list[dict]: The list of chunks matching the search criteria.
    """

    # Create the filter for the search
    db_filter = [{'user_id': int(user_id)}, {'document_id': document_id}] if document_id else [{'user_id': int(user_id)}]
    
    try:
        # Search for similar chunks in the database
        cursor = my_collection.find(
            {"$and": db_filter},
            sort={"$vectorize": query},
            limit=int(limit),
            projection={"$vectorize": True},
            include_similarity=True,
        )
        
    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}') 
    
    # Cursor is closed when called
    return list(cursor)



def search_by_index(index: id_type, document_id: str = None, user_id: id_type = 0) -> list[dict]:
    """
    Search for a chunk by index in the database.

    Args:
        index (id_type): The index of the chunk to search for.
        document_id (str, optional): The document ID to search in. Defaults to None.
        user_id (id_type, optional): The user ID to search for. Defaults to 0.

    Returns:
        list[dict]: The list of chunks matching the search criteria.
    """
    # Create the filter for the search
    if document_id:
        db_filter = [{'user_id': user_id}, {'chunk_id': index},  {'document_id': document_id}]    
    else:
        db_filter = [{'user_id': user_id}, {'chunk_id': index}] 
    
    # Execute the search
    try:
        cursor = my_collection.find(
            {"$and": db_filter},
            limit=1,
        )
        
    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
    
    # Cursor is closed when called
    return list(cursor) 
