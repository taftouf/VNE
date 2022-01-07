import socket
import sys
import threading
from _thread import *
import tkinter as tk
from queue import Queue
from tkinter.messagebox import *
import os
import csv


def get_names(l):
    i = 0
    names = []

    str = "".join(l)
    n = str.split()
    for x in n:
        if i != 1:
            i = i + 1
        else:
            i = i + 1
            names.append(x)

    if names:
        return names[0]


def get_info():
    names = []
    list_info = []
    info = {}
    i = 0
    os.system("virsh list --all > ./output_file.cvs")
    reader = csv.reader(open(r"output_file.cvs"))
    for raw in reader:
        if i < 2:
            i += 1
        else:
            nom = get_names(raw)
            if nom:
                names.append(nom)

    for x in names:
        os.system("virsh dominfo " + x + " > ./output_file.cvs")
        reader = csv.reader(open(r"output_file.cvs"))
        i = 0
        info['Name'] = x
        for raw in reader:
            if i == 5:
                info['CPU'] = "".join(raw).split(":")[1].replace(" ", "")
                i = i + 1
            elif i == 6:
                info['RAM'] = "".join(raw).split(":")[1].replace(" ", "")
                i = i + 1
            else:
                i = 1 + i

        list_info.append(str(info))

    return list_info


class MyThread(threading.Thread):
    def __init__(self, q, ip, port, data):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.q = q
        self._running = True
        self.data = data
        self.s = socket.socket()

    def run(self):
        self.conn_server()

    def conn_server(self):

        try:
            print(self.ip)
            self.s.connect((self.ip, self.port))
        except socket.error as e:
            print(str(e))
            sys.exit(-1)

        while self._running:
            response = self.s.recv(1024)
            if not response:
                pass
            else:
                showinfo(title="INP", message="Resquest to " + self.ip)
                self.q.put(response.decode('utf-8'))
                self.data = get_info()
                self.s.send(str.encode(str(self.data)))

        self.s.close()
        sys.exit(-1)

    def stop(self, data):
        self.data = data
        self._running = False
        print("thread closed")


class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.ip = ""
        self.f1 = ""
        self.conn = False
        self.thread1 = ""
        self.thread2 = ""
        self.data = ""
        self.creer_widgets()

    def creer_widgets(self):

        # frame
        self.f1 = tk.Frame(background="", highlightbackground="black", highlightthickness=1)
        f2 = tk.LabelFrame(text="", width=600, height=210)

        # frame position
        self.f1.pack(fill="both", expand=True, padx=20, pady=20)
        f2.place(in_=self.f1, anchor="c", relx=.5, rely=.5)

        # frame color
        self.f1.configure(bg='red')

        # content of frame2
        tk.Label(f2, text=" Server addr ").place(in_=f2, anchor="nw", relx=0.22, rely=0.08)
        self.ip = tk.Entry(self)
        self.ip.place(in_=f2, anchor="nw", relx=0.5, rely=0.08)
        tk.Button(self, text="Connect", width=10, command=self.connect).place(in_=f2, anchor="nw", relx=0.22, rely=0.5)
        tk.Button(self, text="Disconnect", width=10, command=self.disconnect).place(in_=f2, anchor="nw", relx=0.6,
                                                                                    rely=0.5)

    def send_data(self, q):
        while self.conn:
            print(q.get())
        sys.exit(-1)

    # connect to the server
    def connect(self):
        if not self.conn:
            try:
                socket.inet_aton(self.ip.get())
                port = 1233
                self.conn = True
                q = Queue()
                self.data = "INPs"
                self.thread1 = MyThread(q, self.ip.get(), port, self.data, )
                self.thread1.start()
                # start_new_thread(self.send_data, (q,))

                self.f1.configure(bg='green')
            except socket.error:
                showerror(message="address IP is invalid", icon="error")
        else:
            showerror(message="Your are already connected ", icon="error")

    # close connection
    def disconnect(self):
        if self.conn:
            self.conn = False
            self.data = -1
            self.thread1.stop(self.data)
            self.f1.configure(bg='red')
        else:
            showerror(message="Your are already disconnected ", icon="error")


if __name__ == "__main__":
    app = Application()
    app.geometry('700x300')
    app.resizable(0, 0)
    app.title("INP :-)")
    app.mainloop()
