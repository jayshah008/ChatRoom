import threading
import socket
import logging
import datetime


logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def send_private_message(sender,recipient,message):
    for client,nickname in zip(clients,nicknames):
        if nickname == recipient:
            try:
                client.send(f'Private message sent from {sender}:{message}'.encode('ascii'))
            except:
                continue

def remove(client):
    if client in clients:
        clients.remove(client)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                message = message.decode('ascii')
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp

                if message.startswith('/msg'):
                    parts = message.split()
                    if len(parts) >= 3:
                        recipient = parts[1]
                        message_body = ' '.join(parts[2:])
                        send_private_message(nicknames[clients.index(client)], recipient, message_body)
                elif message.startswith("QUITCHATROOM"):
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname = nicknames[index]
                    broadcast(f'{nickname} has left the chat!'.encode('ascii'))
                    nicknames.remove(nickname)
                    break
                else:
                    print(message)
                    broadcast(f'{message}'.encode('ascii'))
                    logging.info(f'Broadcasted: {message}')

            else:
                remove(client)
        except Exception as e:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            logging.error(f'Error: {e}')
            break


def recieve():
    while True:
        client, addr  = server.accept()
        print(f"Connected with {str(addr)}")
        print("-----WARNING: PLEASE DO NOT USE THE QUITCHATROOM COMMAND AS THERE ARE SOME FIXES TO DO.--------")
        print("USE README TO UNDERSTAND MORE ON IT")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the chat'.encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server is listening...")
recieve()