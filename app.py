from fastapi import FastAPI
from pydantic import BaseModel
import openai,os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
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
async def get_answer(messages: list):
    resp = await openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = messages
        )
    reply = resp.get('choices')[0].get('message').get('content')
    return reply
        
# @app.post('/text_to_voice')
# async def convert_text_to_voice(text):
#     resp = await 

# if __name__=='__main__':
    # conversation_status = True
    # new_conv = chat_gpt_conversation()
    # while conversation_status:
    #     question = text_question()
    #     new_conv.get_chatgpt_resp(question)
    #     conversation_status = False if input('Continue?') in ['No','NO','no'] else True
    #     print('Conversation ends') if not conversation_status else print('')

