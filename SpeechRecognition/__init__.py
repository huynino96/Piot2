import speech_recognition as sr
import os


'''
This class is used to interacting with the Google Cloud Speech to Text API
to detect users' speech input
'''


class SpeechRecognition:
    class ApiConnectionError(Exception):
        pass

    class CanNotRecognizeError(Exception):
        pass

    def __init__(self, credential_json_url, time_out):
        # Read the google credential file, to get it content
        with open(credential_json_url, 'r') as file:
            self.__credential_string = file.read()
        self.__time_out = time_out

        # Create a recognizer and microphone instance
        self.__recognizer = sr.Recognizer()

        # We set this mic to these settings to comply to Google API's constraints
        # The default setting won't allow us to use this API
        self.__mic = sr.Microphone(device_index=None, sample_rate=48000, chunk_size=1024)

    def recognize(self, prompt):
        with self.__mic as source:
            # Adjust noises for more accurate recognition
            self.__recognizer.adjust_for_ambient_noise(source)
            try:
                print(prompt)   # Display a prompt to suggest user what to say
                audio = self.__recognizer.listen(source)    # Listen to our mic and recognize speech
                # Use the API to detect speech
                # The json content of we have read is the credentials we will pass to the function
                text = self.__recognizer.recognize_google_cloud(audio, credentials_json=self.__credential_string)
                return str(text).strip()  # Convert to string and remove trailing space
            except sr.RequestError as e:
                raise SpeechRecognition.ApiConnectionError()  # Throw an error if not connected to the API
            except sr.UnknownValueError as e:
                raise SpeechRecognition.CanNotRecognizeError()   # Throw an error if not can not recognize


if __name__ == '__main__':
    rg = SpeechRecognition(credential_json_url="{}".
                          format(os.path.join(os.path.abspath(os.path.dirname(__file__)), "service_account_key.json")),
                          time_out=3)
    print(rg.recognize("Listening!!! Say something"))
