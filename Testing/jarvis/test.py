import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(sample_rate=41000) as source:
    audio = r.listen(source)
    f = r.recognize_google(source)
    print(f)