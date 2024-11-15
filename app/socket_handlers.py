from flask import request
from app import socketio, socket_manager
from app.utils import bcolors

@socketio.on('connect')
def handle_connect():
    print(f"{bcolors.OKBLUE}Client {request.sid} connected{bcolors.ENDC}")
    socketio.emit('message', {'data': 'Client connected!'})


@socketio.on('disconnect')
def handle_disconnect():
    socketio.emit('message', {'data': 'Client disconnected!'})
    

@socketio.on('disconnect', namespace='/speech')
def handle_disconnect():
    socket_manager.disconnect_socket(request.sid)
    socketio.emit('message', {'data': 'Client disconnected!'})
    
    
@socketio.on('transcription_event', namespace='/speech')
def handle_transcription_event(json):
    socket_manager.transcription_socket(request.sid, json['data'])