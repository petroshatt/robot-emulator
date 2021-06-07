#!/usr/bin/env python3
import json
import socket
import re


global finished
finished = False



def run_TCP(PORT, stop_thread):

    global finished

    s = socket.socket()

    PORT = int(PORT)

    print("\n--------------- File Exchange ---------------\n")
    print("Server is listening on port :", PORT, "\n")
    s.bind(('', PORT)) 
    s.listen(10)


    #while True:

    conn, addr = s.accept()
    input_var = ''

    print("\nCopied file name will be json.json at server side\n")

    # Send a hello message to client
    msg = "\n\n|---------------------------------|\nClient[IP address: "+ addr[0] + "]\n"    
    conn.send(msg.encode())
    
    # Receive any data from client side
    RecvData = conn.recv(1024*1024)
    while RecvData:
        input_var += str(RecvData)
        RecvData = conn.recv(1024*1024)

    print("File has been copied successfully \n")


    #Allages
    input_var = re.sub(r"\s+", "", input_var).replace('\\n','').replace("'b'",'').replace('\\r','')[2:][:-1]

    #print(input_var)

    conn.close()
    return input_var,True


    

#if __name__ == "__main__":       

#    run_TCP(9898,True) 
