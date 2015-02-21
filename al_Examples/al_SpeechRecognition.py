#!/usr/bin/python
#
# Example for Speech Recognition
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import speech_recognition as sr

r = sr.Recognizer()
with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
    audio = r.record(source)                        # extract audio data from the file

try:
    print("Transcription: " + r.recognize(audio))   # recognize speech using Google Speech Recognition
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")
