import azure.cognitiveservices.speech as speechsdk

class assistant_speaker:
    def __init__(self, key, region, voice_name="en-US-AriaNeural"):
        # Creates an instance of a speech config with specified subscription key and service region.
        self.speech_key = key
        self.service_region = region

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.service_region)
        self.speech_config.speech_synthesis_voice_name = voice_name
    
    def speak_default(self, text):
        # use the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config)

        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

