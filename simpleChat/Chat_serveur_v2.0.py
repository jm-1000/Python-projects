# Auteur : JM-1000


import socket, threading
from time import sleep

def reception():
    serveur.listen()
    print('Serveur is listening...')
    while serveur_stop:
        cliente,adresse=serveur.accept()
        print(f'Connecté à {adresse}')
        thread=threading.Thread(target=connection_cliente,args=([cliente,adresse],),daemon=True)
        thread.start()
    return 0


def connection_cliente(idcliente):
        cliente,adresse=idcliente[0],idcliente[1]
        try:
            cliente.send('&key3#'.encode())
            nickname=cliente.recv(2048).decode()
        except:
            return 0
        
        if nicknames.__contains__(nickname):
            cliente.send('Nickname déjà utilisé !'.encode())
            sleep(0.15)
            connection_cliente([cliente,adresse])

        if cliente_interd.__contains__(nickname):
            cliente.send('Accès refusé!'.encode())
            cliente.close()
            return 1
        
        if nickname=='admin':
            code='&pass3#'
            for i in range(3):
                try:
                    cliente.send(code.encode())
                    if cliente.recv(2048).decode()=='x':
                        break
                    else:
                        if i==2:
                            cliente.send('Accès refusé!'.encode())
                            cliente.close()
                            return 1
                except:
                    cliente.close()
                    return 1   


        cliente.send('Connecté dans le serveur!'.encode())
        diffusion(f'{nickname} est connecté au chat!'.encode())
        nicknames.append(nickname)
        clientes.append(cliente)
        print(" Nickname d'adresse ",adresse,' est ',nickname)
        chat(cliente)

def diffusion(messg):
    for cliente in clientes:
        cliente.send(messg)


def chat(cliente):
    control=True
    if control:
        index=clientes.index(cliente)
        nickname=nicknames[index]
        control=False

    while True:
        try:
            msg=cliente.recv(2048)
            txt=msg.decode()
            if nickname=='admin' and txt[7:8]=="/" :
                admin_options(txt,cliente)
            elif len(txt)==len(nickname)+2:
                pass
            else:
                diffusion(msg)
        except:
            try:
                clientes.remove(cliente)
                diffusion(f'{nickname} a sorti du chat!'.encode())
            except:
                break
            print(f'{nickname} desconnecté!')
            nicknames.remove(nickname)
            print('Clientes connectés: ',nicknames)
            cliente.close()
            break

def admin_options(option,admin):
    if option.__contains__('/l'):
        for nickname in nicknames:
          if nickname=='admin':
              admin.send(f'Clientes connectés: {nicknames}'.encode())
              break
    for nickname in nicknames:
          if nickname=='admin':
              continue
          if option[12:].__contains__(nickname):
            if option.__contains__("/ban"):
                cliente_interd.append(nickname) 
            cliente=clientes[nicknames.index(nickname)]
            
            txt=f"{nickname} desconnecté par l'admin!"
            diffusion(txt.encode());print(txt)
            clientes.remove(cliente)
            nicknames.remove(nickname)
            cliente.close()
            break
    if option.__contains__('/stop'):
        global serveur_stop
        serveur_stop=False
        cliente_stop=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cliente_stop.connect((host,port))
    
              
           

host='0.0.0.0'
port=60000
serveur=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serveur.bind((host,port))
clientes,nicknames=[],[]
cliente_interd=[]
serveur_stop=True
reception()

    

