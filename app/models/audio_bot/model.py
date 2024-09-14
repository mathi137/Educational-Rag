from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class AgentTranscriber:
    def __init__(self):
        self.__client = OpenAI(
            api_key=os.getenv('OPENAI_KEY')
        )
        # self.__max_tokens = 800
        self.__temperature = 0.1 


    def audio_to_text(self, audio_path):
        with open(audio_path, 'rb') as audio_file:
            translation = self.__client.audio.translations.create(
                model="whisper-1", 
                file=audio_file,
                temperature=self.__temperature,
                prompt="O aúdio terá falas em português brasileiro."
            )
        result = translation.text
        
        return result


    def text_to_audio(self, text):
        speech_file_path = "./speech.mp3"
        response = self.__client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        
        response.write_to_file(speech_file_path)
        return response
    
    def youtube_to_text(self, url):
        pass
    
    
transcriber_model = AgentTranscriber()


if __name__ == '__main__':
    agent = AgentTranscriber()
    agent.text_to_audio('AÔÔÔ POTENCIAA!')