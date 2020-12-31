import threading

import time

import random

import socket as mysoc

import sys

port=sys.argv[1]
port = int(port)

# server task

def server():

    try:

        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

        print("[S]: Server socket created")

    except mysoc.error as err:

        print('{} \n'.format("socket open error ",err))

    server_binding=('',port)

    ss.bind(server_binding)

    ss.listen(1)

    host=mysoc.gethostname()

    print("[S]: Server host name is: ",host)

    localhost_ip=(mysoc.gethostbyname(host))

    print("[S]: Server IP address is  ",localhost_ip)

    csockid,addr=ss.accept()

    print ("[S]: Got a connection request from a client at", addr)

    f = open("PROJI-DNSRS.txt", "r")
    my_dict = dict()

    for x in f:
        x = x.replace('\r', '').replace('\n', '')
        word = x.split(' ')
        key = word[0]
        key = key.lower()
        my_dict[key] = x

    print(my_dict)

    # send a intro  message to the client.
    while 1:
        data_from_client=csockid.recv(1024)

        msg=data_from_client.decode()
        msg = str(msg)
        print('[S] Client sent:', msg)

        if my_dict.get(msg) is None:
            print("[S]: NO DATA FOUND")
            key = getKeysByValue(my_dict, 'NS')
            print("Found key ", key)
            response = my_dict.get(key)
            csockid.send(response.encode('utf-8'))
        else :
            print("[S]: Found a match")
            response = my_dict.get(msg)
            csockid.send(response.encode('utf-8'))

   # Close the server socket
    print("[S]: Closing server socket connection")

    ss.close()

    print("[S]: Closed server socket connection")

    exit()

def getKeysByValue(dictOfElements, valueToFind):
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if valueToFind in item[1]:
            return item[0]

t1 = threading.Thread(name='server', target=server)

t1.start()
