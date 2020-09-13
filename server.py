import sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

if len(sys.argv) < 2:
    print('No given port number as command line argument: defaulting to 33000')
    PORT = 33000
else:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print('Enter a valid port number.')
        sys.exit(0)

HOST = ''
ADDR = (HOST, PORT)
BUFFER = 1024
MAX_CONNECTIONS = 5

clients = {}


def update_user_list():
    """A hacky way to update the user-list for all clients by broadcasting a message starting with |||."""
    user_comma = ''
    for name in clients.values():
        user_comma += name + ','
    send_all(bytes(f'|||{user_comma}', 'utf8'))


def accept_incoming_connections():
    """Handles incoming connections then spawns new thread for each client."""
    while True:
        client, client_addr = server.accept()
        print(f'Connection from {client}:{client_addr}')
        client.send(bytes('Hello! Please enter your name.', 'utf8'))
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """Handles each client on a separate thread for each."""
    name = client.recv(BUFFER).decode('utf8')
    clients[client] = name
    update_user_list()
    send_all(bytes(f'{name} has joined the chat.', 'utf8'))

    while True:
        msg = client.recv(BUFFER)
        if msg != bytes('[quit]', 'utf8'):
            send_all(msg, name+': ')
        else:
            client.send(bytes('[quit]', 'utf8'))
            client.close()
            del clients[client]
            update_user_list()
            send_all(bytes(f'{name} has left the chat.', 'utf8'))
            break


def send_all(msg, prefix=''):
    for sock in clients:
        sock.send(bytes(prefix, 'utf8') + msg)


if __name__ == '__main__':
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDR)

    server.listen(MAX_CONNECTIONS)
    print('Waiting for connection...')
    accept = Thread(target=accept_incoming_connections)
    accept.start()
    accept.join()
    server.close()
