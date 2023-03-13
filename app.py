from base64 import encode
from fastapi import FastAPI, Form
from pydantic import BaseModel
import openai,os,json
from dotenv import load_dotenv
from typing import List, Dict
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "If you get this message, it means the API works"}

@app.post('/voice_to_text/')
async def convert_voice_to_text(audio_clip: str):
    '''call whisper to convert voice'''
    resp = await openai.Audio.transcribe("whisper-1", audio_clip)
    return resp

@app.post('/conversation/')
def get_answer(data: List[Dict[str, str]]):
    resp = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = data
        )
    reply = resp.get('choices')[0].get('message').get('content')
    print(reply)
    return reply
        
@app.post('/text_to_voice')
def convert_text_to_voice(text):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    # audio_config = speechsdk.audio.AudioOutputConfig(filename='tmp/test.wav')

    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None
    )
    result = speech_synthesizer.speak_text_async(text).get()
    aud_stream = speechsdk.AudioDataStream(result)
    return aud_stream