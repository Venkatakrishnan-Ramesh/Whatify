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

    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350)

        self.pls = tk.Label(self.login,
                            text="Please Login to a Whatify",
                            justify=tk.CENTER,
                            font="Helvetica 12 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username: ", font="Helvetica 11")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Password", font="Helvetica 12")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Helvetica 11", show="*")
        self.roomEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.45)

        self.go = tk.Button(self.login,
                            text="CONTINUE",
                            font="Helvetica 12 bold",
                            command=lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))

        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()

    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))

        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self):
        self.Window.deiconify()
        self.Window.title(" whatify ")
        self.Window.resizable(width=True, height=True)
        self.Window.configure(width=470, height=550, bg="#11201A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",pady=5)

        self.labelHead.place(relwidth=1)
        self.line = tk.Label(self.Window, width=450, bg="#FFFFFF")

        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = tk.Text(self.Window,
                                width=20,
                                height=2,
                                bg="#2e022e",
                                fg="#FFFFFF",
                                font="Helvetica 11",
                                padx=5,
                                pady=5)

        self.check = Button(self.Window, text="Check Sentiment", fg="Black",
                            bg="Red", height=80)

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = tk.Label(self.Window, bg="#ABB2B9", height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.8)

        self.entryMsg = tk.Entry(self.labelBottom,
                                 bg="#2C3E50",
                                 fg="#EAECEE",
                                 font="Helvetica 11")
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.03,
                            rely=0.008,
                            relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom,
                                   text="Send",
                                   font="Helvetica 10 bold",
                                   width=20,
                                   bg="#ABB2B9",
                                   command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.labelFile = tk.Label(self.Window, bg="#ABB2B9", height=70)

        self.labelFile.place(relwidth=1,
                             rely=0.9)
        self.labelFile1 = tk.Label(self.Window, bg="#ABB2B9", height=70)
        self.labelFile2= tk.Label(self.Window, bg="#ABB2B9", height=70)
        self.labelFile1.place(relwidth=1,
                              rely=0.9)
        self.browse = tk.Button(self.labelFile1,
                                text="sentiment",
                                font="Helvetica 10 bold",
                                width=13,
                                bg="#ABB2B9",
                                command=self.detect_sentiment)
        self.browse.place(relx=0.8,
                          rely=0.008,
                          relheight=0.03,
                          relwidth=0.15)
        self.reset=tk.Button(self.labelFile1,text='Reset',font="Helvetica 10 bold",
                                width=9,
                                bg="#ABB2B9",
                                command=self.clear)
        self.reset.place(x=0.99,
                          y=0.2,
                          relheight=0.03,
                          relwidth=0.1)
        self.fileLocation = tk.Label(self.labelFile,
                                     text="Choose file to send",
                                     bg="#2C3E50",
                                     fg="#EAECEE",
                                     font="Helvetica 11")
        self.fileLocation.place(relwidth=0.65,
                                relheight=0.03,
                                rely=0.008,
                                relx=0.011)

        self.negativeField = tk.Entry(self.Window, text="Negative")
        self.negativeField.place(rely=0.9, relx=0.6,
                                 relwidth=0.2)
        self.neutralField = tk.Entry(self.Window)
        self.neutralField.place(rely=0.9, relx=0.13,
                                relwidth=0.2)
        self.positiveField = tk.Entry(self.Window)
        self.positiveField.place(
            rely=0.9, relx=0.35,
            relwidth=0.2)
        self.overallField = tk.Entry(self.Window)
        self.overallField.place(rely=0.95, relx=0.3
                                , relwidth=0.3)

        self.textCons.config(cursor="arrow")
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tk.DISABLED)

    def detect_sentiment(self):

        # get a whole input content from text box
        sentence = self.entryMsg.get()

        # Create a SentimentIntensityAnalyzer object.
        sid_obj = SentimentIntensityAnalyzer()

        # polarity_scores method of SentimentIntensityAnalyzer
        # object gives a sentiment dictionary.
        # which contains pos, neg, neu, and compound scores.
        sentiment_dict = sid_obj.polarity_scores(sentence)

        string = str(sentiment_dict['neg'] * 100) + "% Negative"
        self.negativeField.insert(10, string)

        string = str(sentiment_dict['neu'] * 100) + "% Neutral"
        self.neutralField.insert(10, string)

        string = str(sentiment_dict['pos'] * 100) + "% Positive"
        self.positiveField.insert(10, string)

        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05:
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

    def sendFile(self):
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(str("client_" + os.path.basename(self.filename)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.filename)).encode())
        time.sleep(0.1)

        file = open(self.filename, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state=tk.NORMAL)
        self.textCons.insert(tk.END, "<You> "
                             + str(os.path.basename(self.filename))
                             + " Sent\n\n")
        self.textCons.config(state=tk.DISABLED)
        self.textCons.see(tk.END)

    def sendButton(self, msg):
        self.textCons.config(state=tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)
                            file.write(data)

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END, "<" + str(send_user) + "> " + file_name + " Received\n\n")
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END,
                                         message + "\n\n")

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)

            except:
                print("An error occured!")
                self.server.close()
                break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED)
        while True:
            self.server.send(self.msg.encode())
            self.textCons.config(state=tk.NORMAL)
            self.textCons.insert(tk.END,
                                 "<You> " + self.msg + "\n\n")

            self.textCons.config(state=tk.DISABLED)
            self.textCons.see(tk.END)
            break

    def clear(self):
        self.negativeField.delete(0, END)
        self.neutralField.delete(0, END)
        self.positiveField.delete(0, END)
        self.overallField.delete(0, END)

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    gui = GUI(ip_address, port)


