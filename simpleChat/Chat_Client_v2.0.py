# Auteur : JM-1000


import socket, threading
from getpass import getpass


serveur ='127.0.0.1'
port=60000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((serveur,port))
nickname=''

def receive():
    thread=True; txt="Password : "
    while True:
        try:
            msg=client.recv(2048).decode()

            if msg == '&key3#':
                global nickname
                nickname=input('Nickname : ')      
                client.send(nickname.encode())
            elif msg== '&pass3#':
                client.send(getpass(txt).encode())
                txt='Refusé ! Password : '
            elif msg=="":
                client.close()
                break
            else:
                print(msg)
                if msg=='Accès refusé!':
                    client.close()
                    break
                if msg=='Nickname déjà utilisé !':
                    pass
                elif thread:
                    thread=False
                    write_thread.start()

        except: 
            print('Desconnecté du serveur !')
            client.close()
            break

def write():
    while True:
        try:
            client.send(f'{nickname}: {input()}'.encode())
        except:
            break

receive_thread= threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write,daemon=True)