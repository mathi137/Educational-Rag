from app.models.speech_to_text.model import initialize_azure_recognizer, disconnect_azure_recognizer
from app.utils import bcolors
    
client_recognizers = {}

def disconnect_socket(sid: str) -> None:
    if sid in client_recognizers:
        # Stop and close the Azure recognizer for this client
        disconnect_azure_recognizer(*client_recognizers.pop(sid))
        print(f"{bcolors.OKBLUE}API -> Websocket client {sid} disconnected!{bcolors.ENDC}")
        
        
def transcription_socket(sid: str, audio_data: bytes) -> None:
    if sid not in client_recognizers:
        # Initialize Azure recognizer for this client
        client_recognizers[sid] = initialize_azure_recognizer()
        client_recognizers[sid][0].start_continuous_recognition()
        print(f"{bcolors.OKBLUE}API -> Starting continuous recognition for client {sid}{bcolors.ENDC}")
    
    # Process the audio data for the client's recognizer
    client_recognizers[sid][1].write(audio_data)
    print(f"{bcolors.OKCYAN}Azure Speech Recognition -> Writing audio data into stream for client {sid}{bcolors.ENDC}")
    