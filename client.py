#!/usr/bin/env python3

import sys
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

if len(sys.argv) < 3:
    print('Not given port number or host: defaulting to localhost:33000')
    HOST = '127.0.0.1'
    PORT = 33000
else:
    try:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
    except ValueError:
        print('Usage: ./client.py <HOST> <PORT>')
        sys.exit(0)

BUFFER = 1024
ADDR = (HOST, PORT)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)


def receive():
    while True:
        msg = sock.recv(BUFFER).decode('utf8')
        if msg[:3] == '|||':
            users = msg[3:].split(',')
            users.remove('')
            user_list.delete(1, tk.END)
            for name in users:
                user_list.insert(tk.END, name)
        else:
            msg_list.insert(tk.END, msg)


def send(event=None):
    msg = my_msg.get()
    my_msg.set('')
    sock.send(bytes(msg, 'utf8'))
    if msg == '[quit]':
        sock.close()
        root.quit()


def on_closing(event=None):
    my_msg.set('[quit]')
    send()


root = tk.Tk()
root.title('Tkinter Chat')

messages_frame = tk.Frame(root)

my_msg = tk.StringVar()
my_msg.set('')

scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(fill=tk.BOTH)

entry_field = tk.Entry(messages_frame, textvariable=my_msg)
entry_field.bind('<Return>', send)

send_button = tk.Button(messages_frame, text='Send', command=send)
send_button.pack(side=tk.BOTTOM, fill=tk.X)
entry_field.pack(side=tk.BOTTOM, fill=tk.X)
messages_frame.pack(side=tk.RIGHT)

user_list = tk.Listbox(root, height=15, width=25)
user_list.insert(tk.END, ' --Connected Users-- ')
user_list.pack(side=tk.LEFT, fill=tk.BOTH)

root.protocol('WM_DELETE_WINDOW', on_closing)

Thread(target=receive).start()
root.mainloop()
