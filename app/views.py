from flask import current_app, Blueprint, Response, request

from app.utils import bcolors
from app import manager

import json

main = Blueprint('main', __name__)

@current_app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        return Response(status=200)
    

@main.route('/', methods=['GET'])
def root():
    return 'Endpoint working!'


@main.route('/extract-data', methods=['POST'])
def extract_data_endpoint() -> Response:
    """
    Extract text from a file.

    Args:
        file (File): The file to extract text from.
        user_id (int, str): The ID of the user.

    Returns:
        Response: A JSON response containing the extracted text.
    """
    try:
        file = request.files.get('file')
        user_id = request.args.get('user_id', type=int, default=0)

        if not file:
            return Response('File not provided', status=400)

        file_name = file.filename
        file_contents = file.read()

        response = manager.extract_from_json(file_contents, file_name, user_id)

        return Response(json.dumps(response), status=202)

    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        return Response(json.dumps(str(e)), status=500)
        

@main.route('/extract-from-audio', methods=['POST'])
def extract_from_audio() -> Response:
    """
    Extract text from an audio file.

    Args:
        file (File): The audio file to extract text from.
        user_id (int, str): The ID of the user.

    Returns:
        A JSON response with the extracted text.
    """
    try:
        audio_file = request.files['file']
        user_id = request.args.get('user_id', type=int, default=0)
        
        # Check if the file is valid
        if not audio_file:
            return Response('Audio file not provided', status=400)
        
        file_name = audio_file.filename
        file_bytes = audio_file.read()
        
        # Extract the text from the audio file
        response = manager.extract_from_audio(file_bytes, file_name, user_id)
        
        return Response(json.dumps(response), status=202)
        
    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        return Response(json.dumps(str(e)), status=500)


@main.route('/extract-from-youtube', methods=['POST'])
def extract_from_youtube_endpoint():
    """
    Extract text from a YouTube video.

    Args:
        url (str): The URL of the YouTube video.
        user_id (int, str): The ID of the user.

    Returns:
        Response: A JSON response containing the extracted text.
    """
    try:
        url = request.args['url']
        user_id = request.args.get('user_id', type=int, default=0)

        if not url:
            return Response(status=400)

        response = manager.extract_from_youtube(url, user_id)

        return Response(json.dumps(response), status=202)

    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        return Response(json.dumps(str(e)), status=500)


@main.route('/search', methods=['POST'])
def search_endpoint() -> Response:
    """Search for relevant documents based on a query.

    Args:
        user_id (int, str): The ID of the user.
        limit (int, str): The maximum number of results to return. Defaults to 10.
        document_id (str): The ID of the document to search for. If not provided, search all documents.
        query (str): The query to search for.

    Returns:
        Response: A JSON response containing the search results.
    """
    try:
        user_id = request.args.get('user_id', type=int, default=0)
        limit = request.args.get('limit', type=int, default=10)
        document_id = request.args.get('document_id')
        query = request.args.get('query')

        if not query:
            return Response('Query not provided', status=400)

        response = manager.search_by_query(query, document_id, user_id, limit)

        return Response(json.dumps(response), status=202)

    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        return Response(json.dumps(str(e)), status=500)


@main.route('/chat', methods=['POST'])
def chat_endpoint() -> Response:
    """
    Chat with a document.

    This endpoint generates a chat response based on a document and a question.

    Args:
        user_id (int, str): The ID of the user.
        document_id (str): The ID of the document to chat with.
        question (str): The question to ask the chat bot.

    Returns:
        Response: A JSON response containing the chat response.
    """
    user_id = request.args.get('user_id', type=int, default=0)
    document_id = request.args.get('document_id')
    question = request.args.get('question')

    if not question:
        return Response('Question not provided', status=400)

    try:
        # Get the chat response from the model
        response = manager.chat_botQA(question, document_id, user_id)

        # Return the response as JSON
        return Response(json.dumps(response), content_type='application/json', status=202)

    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        return Response(json.dumps(str(e)), status=500)


@main.route('/chat-stream', methods=['POST'])
def chat_stream_endpoint() -> Response:
    """
    Chat with a document.

    Args:
        user_id (int, str): The ID of the user.
        document_id (str): The ID of the document to chat with.
        question (str): The question to ask the document.

    Returns:
        Response: A text/plain response containing the chat response.
    """
    user_id = request.args.get('user_id', type=int, default=0)
    document_id = request.args.get('document_id')
    question = request.args.get('question')

    if not question:
        return Response('Question not provided', status=400)

    try:
        response = manager.chat_bot_streaming(question, document_id, user_id)
        return Response(response, content_type='text/plain', status=202)

    except Exception as e:
        print(f'{bcolors.FAIL}Exception: {str(e)}{bcolors.ENDC}')
        return Response(json.dumps(str(e)), status=500)
