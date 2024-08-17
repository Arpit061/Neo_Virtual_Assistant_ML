#to import function  CTRL+. , a vs code shortcut

import datetime
import os
import sys
import time
import tokenize
import webbrowser
import elevenlabs
import psutil
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import random
import numpy as np



with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume +1.0)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration= 0.5)
        print("Listening.......", end=" ", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold =True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit=10
        #print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r", end=" ", flush=True)
        print("Recognizing.......", end=" ", flush=True)
        query = r.recognize_google(audio, language = "en-in")
        print("\r", end=" ", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print('Say that again please')  
        return "None"
    return query

#---------------INPUT FOR DAY and TIME -----------------------------------------------

def cal_day(): 
     day = datetime.datetime.today().weekday() +1 #to start it from Monday
     day_dict={
         1:"Monday",
         2:"Tuesday",
         3:"Wednesday",
         4:"Thursday",
         5:"Friday",
         6:"Saturday",
         7:"Sunday"
     }
     if day in day_dict.keys():
         day_of_week = day_dict[day]
         print(day_of_week)
     return(day_of_week)


      
def wishMe():
     hour = int (datetime.datetime.now().hour)
     t = time.strftime("%I:%M:%p")
     day = cal_day()

     if(hour>=0) and (hour<=12) and ('AM' in t):
         speak(f"Good Morning User, It is {day} and the time is{t}")
     elif(hour>=12) and (hour<=16) and ('PM' in t):
         speak(f"Good Afternoon User, It is {day} and the time is{t}") #the f is used to denote the format
     else:
         speak(f"Good evening User , It is {day} and the time is{t}")



def social_media(command):
     #speak("please wait")
     if 'facebook' in command:
         speak("opening facebook")
         webbrowser.open("https://www.facebook.com/")
     elif 'whatsapp' in command:
         speak("opening  whatsapp web")
         webbrowser.open("https://web.whatsapp.com/")
     elif 'discord' in command:
         speak("opening discord server")
         webbrowser.open("https://discord.com/")
     elif 'instagram' in command:
         speak("opening  instagram")
         webbrowser.open("https://www.instagram.com/")
     elif 'youtube' in command:
         speak("opening youtube")
         webbrowser.open("https://youtube.com/")
     elif 'github' in command:
         speak("opening github")
         webbrowser.open("https://github.com/")
     elif 'chrome' in command:
         speak("opening chrome")
         webbrowser.open("https://google.com/")
     else:
         speak("no result found")    

def schedule():
    day = cal_day().lower()
    speak("Sir today's schedule is ")
    week={
    "monday": "sir, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "sir, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "sir, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": "sir, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "sir, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "sir, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "sir, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])


def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')

    elif "notepad" in command:
        speak("opening notepad")
        os.startfile("C:\\Windows\\System32\\notepad.exe")


def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')

    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')



def browsing(query):
    if 'google' in query:
        speak("Boss, what should i search on google..")
        s = command().lower()
        webbrowser.open(f"{s}")
       
    
    
def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"USER, our system have {percentage} percentage battery")

    if percentage>=70:
        speak("Boss, no need to apply charger currently")

    elif percentage>=50 and percentage<=69:
        speak("Boss, keep an eye on the battery percentage")

    elif percentage>=30 and percentage<=49:
        speak("Boss we should connect our system to charging point to charge our battery")

    elif percentage>=20 and percentage<=29:
        speak("Connect the charging point to avoid draining out power")
    else:
        speak("Boss we have very low power, please connect to charging otherwise i am going to sleep...")



if __name__ =="__main__":
     

    wishMe()
    speak("Allow me to introduce myself, My name is , NEO, and i am the virtual AI assistaant that assists you with a variety of tasks as best i can")
    speak("Type about the platform you want to visit or ask me something?")


    while True:
        query =command().lower()
        #query = input("Enter your command -> ")
        if ('facebook' in query ) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query) or ('github' in query) or ('youtube' in query) or ('chrome' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule"  in query):
            schedule()  
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume Increased")

        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume Decreased")

        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume Muted")

        elif("open calculator" in query) or ("open notepad" in query):
            openApp(query)

        elif("close calculator" in query) or ("close notepad" in query):
            closeApp(query)
        
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))

        

        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            speak("please wait")
            condition()
        
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)


        elif "exit" in query:
            sys.exit()        

#speak(" Hello, I am NEO")