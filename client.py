from speaker import assistant_speaker
from dotenv import load_dotenv
import os,json,requests
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream

load_dotenv()
remote_addr = os.getenv('REMOTE_ADDR')

class chat_gpt_conversation:
    def __init__(self, remote_addr=remote_addr):
        self.remote_addr = remote_addr
        self.system_setting = '''
        you are my English teacher. You should follow rules below:
        1. When I start a topic with "Let's talk about XXX" which XXX is referred to the topic,
        our following conversation should centre on this topic.
        '''
        self.conversations = [
            {'role': 'system', 'content': self.system_setting}
        ]

    def add_text_to_conv(self, role, text):
        self.conversations.append(
            {'role': role, 'content': text}
        )

    def add_user_text(self, text):
        self.add_text_to_conv('user', text)

    def add_gpt_text(self, text):
        self.add_text_to_conv('assistant', text)

    def send_text(self, text):
        text_api_url = self.remote_addr + 'conversation'
        self.add_user_text(text)
        resp = requests.post(text_api_url, json=self.conversations)
        print(resp)
        if resp.status_code == 200:
            text = resp.json()
            # print(rep_json)
            self.add_gpt_text(text)
            return text
    
    def convert_text_to_voice(self, text):
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        
        speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config)
        result = speech_synthesizer.speak_text_async(text).get()
        # aud_stream = speechsdk.AudioDataStream(result)
        # return aud_stream

if __name__=="__main__":
    conv = chat_gpt_conversation()
    test_text1 = "Let's talk about soccer. Who is the best player in the world?"
    answer = conv.send_text(test_text1)
    conv.convert_text_to_voice(answer)
    test_text2 = 'I believe only Christian Ronald is the GOAT player. He can play better than any one else'
    answer2 = conv.send_text(test_text2)
    conv.convert_text_to_voice(answer2)
