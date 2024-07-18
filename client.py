import socket 
import time
import threading
import logging
import datetime

logging.basicConfig(filename='client.log',level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

nickname = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

exit_flag = False

def receive():
    global exit_flag
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
                logging.info(f'Received: {message}')

            if message == "QUITCHATROOM":
                exit_flag = True
                break
        except ConnectionResetError:
            break
        except:
            print("Exiting....")
            client.close()
            break

        time.sleep(0.1)

def write():
    global exit_flag
    while True:
        if exit_flag:
            client.close()
            break
        message = input('')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        if message.startswith('/msg'):
            parts = message.split()
            if(len(parts) >= 3):
                recipient = parts[1]
                message_body = ' '.join(parts[2:])
                client.send(f'/msg {recipient} {message_body}'.encode('ascii'))
            else:
                print("Invalid private message format. Use: /msg <recipient> <message>")
        elif message == '/quit':
            exit_flag = True
            client.send(f'QUITCHATROOM'.encode('ascii'))
            client.close()
            break
        elif message == 'NICK':
            client.send(f'NICK'.encode('ascii'))
        elif message == '/help':
            print("--------HERE ARE SOME FUNCTIONS YOU CAN USE---------")
            print("\"/msg <recipeint> <message>\" ----- Send a private message")
            print("\"/quit\" ---- quit the chat")
            print("\"NICK\" ---- Find all the nicknames of people in the chatroom")
        else:
            publicmessage = f'{timestamp} {nickname}:{message}'
            client.send(publicmessage.encode('ascii'))
            logging.info(f'Sent: {publicmessage}')


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
