from queue import Queue
import socket
import time
import tkinter as tk
from tkinter.messagebox import *
from _thread import *
import multiprocessing


def pos(x):
    if x < 0:
        return x*(-1)
    else:
        return x


def tris(x, l):
    x = x*1000000
    l_min = {}
    lf = []
    n = len(l)

    for i in l:
        l_min[i] = pos(x-i)
    while n:
        min_key = min(l_min, key=l_min.get)
        lf.append(min_key)
        l_min.pop(min_key)
        n -= 1
    return lf


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.manager = multiprocessing.Manager()
        self.shared_list = self.manager.list()
        # att server
        self.s = socket.socket()
        self.host = ''
        self.port = 1233
        self.ips = set()
        self.q1 = Queue()
        self.q2 = Queue()
        self.clients = set()
        self.res = []
        self.req = []
        self.f = []
        #
        self.box = ""
        self.result = ""
        self.e1 = ""
        # self.e2 = ""
        self.e3 = ""
        self.e4 = ""
        # self.clicked = tk.StringVar()
        # self.options = ["Ubuntu Server", "Fedora Server"]
        self.widgets()

    def widgets(self):
        f = tk.Frame(background="", highlightbackground="black", highlightthickness=1)
        f.pack(fill="both", expand=True, padx=20, pady=20)
        # part 1
        f1 = tk.LabelFrame(self, text="", width="600", height="180")
        f1.place(in_=f, anchor="c", relx=.5, rely=.2)
        f11 = tk.LabelFrame(text="INP List")
        f11.place(in_=f1, anchor="c", relx=.5, rely=.6)
        start_button = tk.Button(self, text="Start Server", width="20", command=self.start_server)
        start_button.place(in_=f1, anchor="c", relx=.5, rely=.18)
        s = tk.Scrollbar(self)
        s.pack(in_=f11, side="right", fill="both")
        self.box = tk.Listbox(self, width=50, height=5, yscrollcommand=s.set)
        self.box.pack(in_=f11, side="left", fill="y")
        # start_new_thread(self.list_inp, (self.box, self.q1, self.q2,))

        # part 2
        f2 = tk.LabelFrame(self, text="", width="600", height="150")
        f2.place(in_=f, anchor="c", relx=.5, rely=.55)
        # part 1
        tk.Label(f2, text="RAM").place(in_=f2, anchor="nw", relx=0.15, rely=0.18)
        self.e1 = tk.Scale(f2, from_=1, to=32, orient="horizontal")
        self.e1.place(in_=f2, anchor="nw", relx=0.3, rely=0.04)
        # part 2
        tk.Label(f2, text="CPU").place(in_=f2, anchor="nw", relx=0.55, rely=0.18)
        self.e3 = tk.Scale(f2, from_=1, to=10, orient="horizontal")
        self.e3.place(in_=f2, anchor="nw", relx=0.7, rely=0.04)
        # part 3
        send_button = tk.Button(self, text="Send request", width="20", command=self.send_request)
        send_button.place(in_=f2, anchor="nw", relx=0.35, rely=0.6)

        # part 3
        f3 = tk.LabelFrame(self, text="Result", width="600", height="150")
        f3.place(in_=f, anchor="c", relx=.5, rely=.835)
        s2 = tk.Scrollbar(self)
        s2.pack(in_=f3, side="right", fill="both")
        self.result = tk.Listbox(self, width=73, height=6, yscrollcommand=s2.set)
        self.result.pack(in_=f3, side="left", fill="y")

    def threaded_client(self, connection, x):
        connection.sendall(str.encode(str(x)))
        while True:
            data = connection.recv(2048)
            reply = data.decode('utf-8')
            if not reply:
                break
            elif reply == '-1':
                # start_new_thread(self.list_inp, (self.box, ))
                # self.box.insert("end", str(max(self.ips)) + "is Disconnected")
                # self.ips.remove(max(self.ips))
                print(reply)
            else:
                self.req.append(reply)
                if len(self.req) == len(self.clients):
                    for r in self.req:
                        print(r)
                        self.res.append(int(r.split(",")[2].split("}")[0].split(":")[1].split("K")[0].split("'")[1]))
                    
                    self.f = tris(int(self.e1.get()), self.res)
                    for res in self.f:
                        for x in self.req:
                            if res == int(x.split(",")[2].split("}")[0].split(":")[1].split("K")[0].split("'")[1]):
                                self.result.insert("end", str(x))
                else:
                    pass
        connection.close()

    def worker_1(self):
        try:
            self.s.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))

        print('Waiting for a Connection..')
        self.s.listen(5)

        while True:
            client, address = self.s.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            self.box.insert("end", str(address[0]) + "is Connected")
            self.ips.add(address[0])
            self.clients.add(client)
            # q.put(str(address[0]))
        # self.s.close()

    def start_server(self):
        start_new_thread(self.worker_1, ())
        showinfo(title="NVE", message="connection started", icon="info")

    def send_request(self):
        # x = {"ram": self.e1.get(), "disk": self.e2.get(), "cpu": self.e3.get(), "os": self.clicked.get()}
        x = {"ram": self.e1.get(), "cpu": self.e3.get()}
        showinfo(title="VNP", message="Request to INPs", icon="info")
        for i in self.clients:
            start_new_thread(self.threaded_client, (i, x,))


if __name__ == "__main__":
    app = Main()
    app.geometry('700x550')
    app.resizable(0, 0)
    app.title("VNP :-)")
    app.mainloop()
