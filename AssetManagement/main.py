
from multiprocessing import Queue
import pickle
import select
import socket
import threading

receivequeue=Queue()

#region prihvatanje apdejta deviceova
def ListenForMainControlerNotifications():
    HOST=''
    PORT=5017
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening on port 5017 for new notifications.")
    read_list = [ss]
    while True:
        try:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is ss:
                    client_socket, address = ss.accept()
                    read_list.append(client_socket)
                    print( "Connection from", address)
                else:
                    data = s.recv(8192)
                    if data:
                        device=pickle.loads(data)
                        for i in range(0,len(device)):
                            receivequeue.push(i)
                        s.send('ok'.encode())
                        
                    else:
                        read_list.remove(s)
        except:
            print(readable)
#endregion
#region menu
def Menu():
    while(True):
        print("1. Napravi izvestaj.")
        print("2. Broj radnih sati za uredjaj.")
    return
#endregion

if __name__ == "__main__":
    recieveProcess=threading(target=ListenForMainControlerNotifications,args=())
    menuProcess=threading(target=Menu,args=())
