import socket
import tkinter as tk
from tkinter import *
import time
import threading
import os
from tkinter import filedialog
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib.pyplot import text
class GUI:

    def detect_sentiment(self):

        # get a whole input content from text box
        sentence = self.entryMsg.get()

        # Create a SentimentIntensityAnalyzer object.
        obj = SentimentIntensityAnalyzer()

        dict1 = obj.polarity_scores(sentence)

        string = str(dict1['neg'] * 100) + "% Negative"
        self.negativeField.insert(10, string)

        string = str(dict1['neu'] * 100) + "% Neutral"
        self.neutralField.insert(10, string)

        string = str(dict1['pos'] * 100) + "% Positive"
        self.positiveField.insert(10, string)

        # decide sentiment as positive, negative and neutral
        if dict1['compound'] >= 0.05:
            string = "Positive"

        elif sentiment_dict['compound'] <= - 0.05:
            string = "Negative"


        else:
            string = "Neutral"

        self.overallField.insert(10, string)

    def browseFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a file",
                                                   filetypes=(("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
        self.fileLocation.configure(text="File Opened: " + self.filename)

    def clear(self):
        self.negativeField.delete(0, END)
        self.neutralField.delete(0, END)
        self.positiveField.delete(0, END)
        self.overallField.delete(0, END)

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    gui = GUI(ip_address, port)


