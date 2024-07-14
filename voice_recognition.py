import speech_recognition as sr
import time

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def recognize_speech(self, language='en-US'):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  
            audio = self.recognizer.listen(source)
            print("Recognizing...")
            try:
                text = self.recognizer.recognize_google(audio, language=language)
                print(f"You said ({language}):", text)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return ""

    def get_language_choice(self):
        language_map = {
            'english': 'en-US',
            'hindi': 'hi-IN',
            'malayalam': 'ml-IN'
        }
        print("Please say the language you want to use: English, Hindi, or Malayalam.")
        while True:
            language_choice = self.recognize_speech(language='en-US').lower()
            if language_choice in language_map:
                return language_map[language_choice]
            else:
                print("Unsupported language. Please say English, Hindi, or Malayalam.")

if __name__ == "__main__":
    processor = VoiceProcessor()
    
    # Get the language choice from the user
    language = processor.get_language_choice()
    print(f"Language selected: {language}")

    # Pause briefly to ensure the system is ready
    time.sleep(2)

    # Recognize speech in the selected language
    while True:
        print("Please speak now...")
        text = processor.recognize_speech(language=language)
        if text:
            print(f"Recognized text: {text}")
            break
        else:
            print("Please speak again.")
