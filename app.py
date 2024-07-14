from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
CORS(app)

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

voice_processor = VoiceProcessor()

def extract_keywords(text):
    words = word_tokenize(text)
    fashion_keywords = ['fashion', 'style', 'design', 'clothing', 'shirt', 'dress', 'accessories', 'trend', 'latest']
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    fashion_words = [word for word in words if word in fashion_keywords]
    return fashion_words

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    language = 'en-US' 
    text = voice_processor.recognize_speech(language)
    
    if text:
        keywords = extract_keywords(text)
        return jsonify({'keywords': keywords}), 200
    else:
        return jsonify({'keywords': []}), 200  

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
