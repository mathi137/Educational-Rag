import azure.cognitiveservices.speech as speechsdk

from app import socketio
from app.utils import bcolors

from dotenv import load_dotenv
import os

load_dotenv()

# Speech key and region from your Azure Speech Recognition service
speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv('AZURE_SPEECH_KEY'), 
    region=os.getenv('AZURE_SPEECH_REGION')
)

# Configuration for the input audio format. The documentation specifies that you can use GStreamer (It also needs to be installed locally) to encode other formats to PCM (Pulse Code Modulation). 
# Here I'm using speechsdk.AudioStreamContainerFormat.ANY since i'm sending streaming data using the audio/webm;codecs:opus format directl, that is supported for most of the modern browsers 
audio_format = speechsdk.audio.AudioStreamFormat(compressed_stream_format=speechsdk.AudioStreamContainerFormat.ANY) # To receive audio data in any format and process them with GStreamer
push_stream = speechsdk.audio.PushAudioInputStream(audio_format) # Creates an audio stream to send data to the speech service
audio_config = speechsdk.audio.AudioConfig(stream=push_stream) # Adjust the audio config using the recently created stream


def initialize_azure_recognizer() -> tuple: # loop, queue    
    # Creates a speech recognizer client for the speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config,
        language="pt-BR" # Change to your desired language if supported. If not specified, 'en-US' will be used by default.
    )

    # Callbacks for the speech recognizer. They are automatically triggered based on event type
    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        """
        Triggered everytime the recognizer has processed a set of audio chunks and recognized part of the speech
        """
        print(f"{bcolors.OKGREEN}Azure Speech Recognition -> Recognizing: {evt.result.text}{bcolors.ENDC}")
        socketio.emit('transcription', {'data': evt.result.text}, namespace='/speech')  # Emit to client


    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        """
        Triggered when the speech recognition has processed an audio fragment and recognized the text in its entirety
        """
        print(f"{bcolors.OKGREEN}Azure Speech Recognition -> Recognized: {evt.result.text}{bcolors.ENDC}")
        # asyncio.run_coroutine_threadsafe(queue.put(evt.result.text), loop)
        socketio.emit('transcription_finished', {'data': evt.result.text}, namespace='/speech')  # Emit to client
        
        
    def stop_cb(evt: speechsdk.SessionEventArgs):
        """
        Triggered when speech recognition session is stopped
        """
        print(f"{bcolors.WARNING}Azure Speech Recognition -> Session stopped due websocket close: {evt}{bcolors.ENDC}")

    def canceled_cb(evt: speechsdk.SessionEventArgs):
        """
        Triggered when the speech recognition session is cancelled due to an error
        """
        print(f"{bcolors.FAIL}Azure Speech Recognition -> Session canceled due an error: {evt}{bcolors.ENDC}")

    # Connect callbacks to the speech recognizer to be triggered when an event occurs.
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(canceled_cb)

    return speech_recognizer, push_stream


def disconnect_azure_recognizer(recognizer, push_stream):
    print(f"{bcolors.FAIL}Azure Speech Recognition -> Stream closed{bcolors.ENDC}")
    push_stream.close()
    print(f"{bcolors.OKBLUE}API -> Stopping continuous recognition...{bcolors.ENDC}")
    recognizer.stop_continuous_recognition()
    print(f"{bcolors.OKBLUE}API -> Continuous recognition stopped!{bcolors.ENDC}")