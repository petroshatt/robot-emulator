#!/usr/bin/env python3

import socket

global finished
finished = False

def run_TCP(PORT, stop_thread):

    global finished

    s = socket.socket()

    PORT = int(PORT)

    print("\n--------------- File Exchange ---------------\n")
    print(" Server is listing on port :", PORT, "\n")
    s.bind(('', PORT)) 
    s.listen(10)


    while True:

        conn, addr = s.accept()

        if finished == False:

            file = open("../data/json.json", "wb")
            print("\n Copied file name will be json.json at server side\n")

            # Send a hello message to client
            msg = "\n\n|---------------------------------|\n Client[IP address: "+ addr[0] + "]\n"    
            conn.send(msg.encode())
            
            # Receive any data from client side
            RecvData = conn.recv(1024)
            while RecvData:
                file.write(RecvData)
                RecvData = conn.recv(1024)

           
            file.close()
            print(" File has been copied successfully \n")

            finished = True

            conn.close()

        if stop_thread == True:
            break
