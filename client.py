from speaker import assitant_speaker
from dotenv import load_dotenv
import os
import requests

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
        self.add_text_to_conv('assitant', text)

    def send_text(self, text):
        text_api_url = self.remote_addr + 'conversation'
        print(f'text_api_url: {text_api_url}')
        self.add_user_text(text)
        reply = requests.post(text_api_url,data=self.conversations)
        self.add_gpt_text(reply)
        print(reply)

    def send_voice(self, audio_clip):
        pass

if __name__=="__main__":
    conv = chat_gpt_conversation()
    test_text1 = "Let's talk about soccer. Who is the best player in the world?"
    conv.send_text(test_text1)

