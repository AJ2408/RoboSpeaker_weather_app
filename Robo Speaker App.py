import pyttsx3
import speech_recognition as sr
import requests
import json

engine = pyttsx3.init('sapi5')

# Getting properties with the help of getProperty method
voices = engine.getProperty('voices')
voice = engine.getProperty('voice')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

# setting or tunning the properties with setProperty method of robo speaker.
engine.setProperty(name='voices', value=voices)
engine.setProperty(name='voice', value=voices[1].id)
engine.setProperty(name='rate', value=130)
engine.setProperty(name='volume', value=1.0)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    """ It takes microphone input from user and returns string output."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")

    except Exception as e:
        # print(e)             # Comment it to not show error name in console
        speak('Say that again please...')
        return takeCommand()   # To restart to listening without interrupting after exception error.
    return query


def get_city_name_from_speech():
    """Gets the city name from speech recognition."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print('Recognizing...')
        city_name = r.recognize_google(audio, language='en-in')
        print("The city name is: {}".format(city_name))
    except sr.UnknownValueError:
        speak("Could not understand your speech.")
        return get_city_name_from_speech()
    except sr.RequestError:
        speak("Speech recognition error.")
        return get_city_name_from_speech()
    return city_name


if __name__ == '__main__':
    speak('System Activated!')
    speak("Welcome to RoboSpeaker 2.O Created by Ajay")
    speak('What do you want me to do sir!...')

    while True:
        query = takeCommand().lower()

        # This block is for weather report. Just say 'weather' in your command statement.
        if 'weather'.lower() in query:
            # Say the city name here...
            speak('Which city My-lord!...')

            try:
                city_name = get_city_name_from_speech()
                speak(f"Searching weather of {city_name}")
                url = f"http://api.weatherapi.com/v1/current.json?key='weatherapi key here'&q={city_name}"
                r = requests.get(url)
                # print(r.text)
                result = json.loads(r.text)
                w = result['current']['temp_c']
                speak('Alright')
                speak('According to weather report...')
                speak(f'The weather of {city_name} is {w} degrees')

            except Exception as e:
                speak(f'Sorry sir! an error occur regarding weather report of {city_name} and the error is {e}')

            speak("any other city's weather you want to find")
            # Here if you want to find another city's weather, you'll have to say 'weather' again in your sentence.

        elif 'Terminate'.lower() in query:
            # This statement will end the loop of weather searching block.
            speak('Then any other command sir...')

        # You can add multiple elif statements to give commands.

        elif 'Deactivate'.lower() in query:
            # This will Shut Down the Robo.
            speak("System Deactivated!")
            exit()
