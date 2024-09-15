from flask import current_app, Blueprint, Response, request
import json

from app import manager

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def root():
    return 'Endpoint working!'


@main.route('/extract-data', methods=['POST'])
def extract_data():
    try:    
        file = request.files['file']
        user_id = request.args.get('user_id') or 0
        # other_data = request.form.to_dict()

        if not file:
            return Response(status=400)
        
        file_name = file.filename
        file_bytes = file.read()
        
        response = manager.extract_data_to_json(file_bytes, file_name, user_id)
        
        return Response(json.dumps(response), status=202)
        
    except Exception as e:
        print(f'Exception: {str(e)}')
        return Response(json.dumps(str(e)), status=500)
        

@main.route('/extract-from-audio', methods=['POST'])
def extract_from_audio():
    try:    
        file = request.files['file']
        user_id = request.args.get('user_id') or 0
        print('extract-from-audio:', user_id)
        

        if not file:
            return Response(status=400)
        
        file_name = file.filename
        file_bytes = file.read()
        
        response = manager.extract_data_to_audio(file_bytes, file_name, user_id)
        
        return Response(json.dumps(response), status=202)
        
    except Exception as e:
        print(f'Exception: {str(e)}')
        return Response(json.dumps(str(e)), status=500)


@main.route('/extract-from-youtube', methods=['POST'])
def extract_from_youtube():
    try:    
        url = request.args.get('url')
        user_id = request.args.get('user_id') or 0
        print('extract-from-youtube:', user_id)

        if not url:
            return Response(status=400)
        
        response = manager.extract_from_youtube(url, user_id)
        
        return Response(json.dumps(response), status=202)
        
    except Exception as e:
        print(f'Exception: {str(e)}')
        return Response(json.dumps(str(e)), status=500)


@main.route('/search', methods=['POST'])
def search():
    try:
        user_id = request.args.get('user_id') or 0
        limit = request.args.get('limit') or 5
        document_id = request.args.get('document_id')
        query = request.args.get('query')
        
        response = manager.search_by_query(query, document_id, user_id, limit)
        
        return Response(json.dumps(response), status=202)
    
    except Exception as e:
        print(f'Exception: {str(e)}')
        return Response(json.dumps(str(e)), status=500)
    

@main.route('/chat', methods=['POST'])
def chat():
    try:
        chat_history = request.get_json(silent=True)
        
        user_id = request.args.get('user_id') or 0
        document_id = request.args.get('document_id')
        question = request.args.get('question')
        
        response = manager.chat_botQA(question, document_id, user_id, chat_history)
        
        return Response(json.dumps(response), status=202)
    
    except Exception as e:
        print(f'Exception: {str(e)}')
        return Response(json.dumps(str(e)), status=500)
