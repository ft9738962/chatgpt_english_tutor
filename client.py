from speaker import assitant_speaker
from dotenv import load_dotenv
import os

load_dotenv()
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')

class chat_gpt_conversation:
    def __init__(self):
        self.system_setting = 'you are '
        self.conversations = [
            {'role': 'system', 'content': self.system_setting}
        ]
        self.assitant_speaker = assitant_speaker(
            key = speech_key,
            region = speech_region
        )

    def add_answer_to_conv(self, answer):
        self.conversations.append(
            {'role': 'assistant', 'content': answer}
        )

    def get_chatgpt_resp(self, question):
        self.conversations.append(
                {'role': 'user', 'content': question}
            )
        print(f'User: {question}')

        answer = response['choices'][0]['message']['content']
        self.assitant_speaker.speak_default(answer)
        self.add_answer_to_conv(answer)
        print(f'ChatGPT: {answer}\n\n')

if __name__=="__main__":
    pass