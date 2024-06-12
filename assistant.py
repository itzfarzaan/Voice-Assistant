import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import time
import requests
from bs4 import BeautifulSoup
import os
import threading
from words2num import words2num


# BASIC INFO
# Say 'Alexa' to let the program know you are ready to say a command 
# Say the command only after it says "speak"
# If you want to google anything, say "search" followed by your query

engine = pyttsx3.init()
if not engine._inLoop:
    engine.runAndWait()

listener = sr.Recognizer()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
interaction_counter = 0
alarms = []
api = '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'
alarm_flag = False



def talk(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    engine.say(text)
    engine.runAndWait()


# If you want to remove the wake up word
# with sr.Microphone() as source:
            # listener.adjust_for_ambient_noise(source, duration=1)
            # print('Speak...')
            # voice = listener.listen(source, timeout=10, phrase_time_limit=10)
            # command = listener.recognize_google(voice)
            # command = command.lower()
            # if 'alexa' in command:
            #     command = command.replace('alexa', '')



def take_command():
    command=""
    try:
        while True:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=2)
                print('Waiting for a wake-up call...')
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
                if 'alexa' in command:
                    command = command.replace('alexa', '')
                    print('Speak..')
                    voice = listener.listen(source, timeout=10, phrase_time_limit=10)
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    print(f'Command: {command}')
                    break  

    except sr.UnknownValueError:
        print("Cannot Understand Audio.")
        talk("Cannot Understand Audio.")
        command = ""

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        talk(f"Could not request results from Google Speech Recognition service; {e}")
        command = ""

    except:
        pass
    return command


def take_command2():
    command = ""
    while True:
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=1)
                print('Speak...')
                voice = listener.listen(source, timeout=10, phrase_time_limit=10)
                transcribed_command = listener.recognize_google(voice)
                transcribed_command = transcribed_command.lower()

                try:
                    # Use words2num to convert spoken numbers to digits
                    transcribed_command = words2num(transcribed_command)
                except ValueError:
                    pass

                print(f"Command: {transcribed_command}")
                command = transcribed_command
                break
        except sr.UnknownValueError:
            print("Cannot Understand Audio. Please repeat.")
            talk("Cannot Understand Audio. Please repeat.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            talk(f"Could not request results from Google Speech Recognition service; {e}")
            command = ""
        except:
            pass
    return command




def activate_assistant():
    global interaction_counter
    starting_chat_phrases = ["how may I assist you?",
               "What can I do for you?",
               "How can I help you?",
               "what can I do for you today?",
               "what's on your mind today?",
               "How may I be of assistance to you right now?",
               "How can I assist you today",
               "How can I make your day easier?",]

    continued_chat_phrases = ["yes", "yes, sir", "I'm all ears"]

    random_chat = ""
    if(interaction_counter == 0):
        random_chat = random.choice(starting_chat_phrases)
        interaction_counter = 1
    else:
        random_chat = random.choice(continued_chat_phrases)
    
    return random_chat




#Alarm feature is not yet ready, Ignore this section.
def add_alarm():
    print("Please specify the hour for the alarm (in 24-hour format).")
    talk("Please specify the hour for the alarm (in 24-hour format).")
    hour = take_command2()

    print("Please specify the minute for the alarm.")
    talk("Please specify the minute for the alarm.")
    minute = take_command2()

    print("Please provide a label or description for the alarm.")
    talk("Please provide a label or description for the alarm.")
    alarm_label = take_command()


    alarm_time = f"{hour}:{minute}"
    alarms.append({'time': alarm_time, 'label': alarm_label})
    print(f"Alarm set for {alarm_time} with label {alarm_label}.")
    talk(f"Alarm set for {alarm_time} with label {alarm_label}.")

def check_and_trigger_alarms():
    global alarm_flag
    while True:
        current_time = datetime.datetime.now().strftime('%H:%M')
        for alarm in alarms:
            if current_time == alarm['time']:
                alarm_flag = True
                alarms.remove(alarm)
                print(f"Alarm: {alarm['label']} is going off!")
                speak(f"Alarm: {alarm['label']} is going off!")
        time.sleep(5)





def query(user_query):
    
  if '+' or '-' or 'multiplied by' or '/' in user_query:
    user_query = user_query.replace("+","%2B")
    user_query = user_query.replace("multiplied by","*")

    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    
    result_divs = soup.find_all(class_='Ww4FFb vt6azd')

    if not result_divs:
     result_divs = soup.find_all(class_='Z0LcW t2b5Cf')

    if not result_divs:
     result_divs = soup.find_all(class_='hgKElc')

    if not result_divs:
     result_divs = soup.find_all(class_='PZPZlf hb8SAc')

    if not result_divs:
     result_divs = soup.find_all(class_='z7BZJb XSNERd')

    # if not result_divs:
    #  result_divs = soup.find_all(class_='NPb5dd')

    if result_divs:
      for result in result_divs:
          
        gresult = result.get_text()
        if 'Description' or 'Wikipedia' or 'Feedback' in gresult:
            gresult = gresult.replace("Description","")
            gresult = gresult.replace("Wikipedia","")
            gresult = gresult.replace("Feedback","")
        print(gresult)
        talk(gresult)

    else:
        print("Sorry, no results found. Please be more specific.")
        talk("Sorry, no results found. Please be more specific.")





def run_alexa():
    global alarm_flag
    # print('Hello, I am your personal voice assistant.')
    # talk('Hello, I am your personal voice assistant.')
    # intro = activate_assistant()
    # print(intro)
    # talk(intro)


    import threading
    alarm_thread = threading.Thread(target=check_and_trigger_alarms)
    alarm_thread.start()

    while True: 

        if alarm_flag:
            talk("Please say a command.")
            command = take_command()
            alarm_flag = False
        else:
            command = take_command()


        if 'play' in command:
            song = command.replace('play', '')
            os.system('cls' if os.name == 'nt' else 'clear')
            talk('playing ' + song)
            talk('playing ' + song)
            pywhatkit.playonyt(song)

        elif 'set alarm' in command:
            add_alarm()

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(command)
            os.system('cls' if os.name == 'nt' else 'clear')
            print('The current time is ' + time)
            talk('The current time is ' + time)

        elif 'search' in command:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(command)
            command = command.replace("search","")
            query(command)

        elif 'who is' in command:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(command)
            person = command.replace('who is', '')
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError:
                print('Multiple matches found. Please be more specific.')
                talk('Multiple matches found. Please be more specific.')
            except wikipedia.exceptions.HTTPTimeoutError:
                print('Wikipedia search timed out. Please try again.')
                talk('Wikipedia search timed out. Please try again.')
            except wikipedia.exceptions.PageError:
                print('No result found in Wikipedia.')
                talk('No result found in Wikipedia.')

        elif 'date' in command:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(command)
            current_date = datetime.datetime.now().strftime('%B %d, %Y')
            print('Today is ' + current_date)
            talk('Today is ' + current_date)

        elif 'joke' in command:
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(command)
            joke = pyjokes.get_joke()
            print(joke)
            talk(joke)

        elif 'stop' in command:  
            print('Turning off.')
            talk('Turning Off')
            break

        else:
            print('Please Repeat.')
            talk('Please Repeat')

if __name__ == '__main__':
    # Run the alarm_thread_function in a separate thread
    alarm_thread = threading.Thread(target=check_and_trigger_alarms)
    alarm_thread.start()
    run_alexa()
