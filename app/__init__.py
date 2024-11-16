from flask import Flask
from flask_socketio import SocketIO
# from flask_cors import CORS
import os

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # CORS(app, resources={r'/*': {'origins': '*'}})
    
    with app.app_context():
        from app.views import main
        app.register_blueprint(main)
        
    from app.socket_handlers import socketio
    socketio.init_app(app)

    return app
