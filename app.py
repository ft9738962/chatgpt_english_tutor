from fastapi import FastAPI, Form
from pydantic import BaseModel
import openai,os
from dotenv import load_dotenv
from typing import List, Dict

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
        
# @app.post('/text_to_voice')
# async def convert_text_to_voice(text):
#     resp = await 