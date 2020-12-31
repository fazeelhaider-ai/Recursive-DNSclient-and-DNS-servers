import socket as mysoc
import threading
import time
import random

import sys
import pdb


rs_hostname=sys.argv[1]
rs_port=sys.argv[2]
rs_port = int(rs_port)
ts_port=sys.argv[3]
ts_port = int(ts_port)


#client function

def client():

    try:

        cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

        print("[C]: RS socket created")

        ts=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

        print("[C]: TS socket created")

    except mysoc.error as err:

        print('{} \n'.format("socket open error ",err))

#defining the port for rs

    #port = 50007

    #rs_hostname = mysoc.gethostname()

    sa_sameas_myaddr =mysoc.gethostbyname(rs_hostname)

# connect to the server on local machine

    server_binding=(sa_sameas_myaddr,rs_port)

    cs.connect(server_binding)

    f = open("PROJI-HNS.txt", "r")

    f1 = open("RESOLVED.txt", "w")

    ts_hostname = ''
    hostname_bool = 0

    for x in f:

        #replacing new line in files
        x = x.replace('\r', '').replace('\n', '')
        x = x.lower()
        print("[C]: Sending message ", x)
        #sending to server
        cs.send(x.encode())
        print("[C]: Message sent")

        #recieving from server
        data_from_server=cs.recv(100)

        fm = str(data_from_server.decode('utf-8'))

        print("[C]: Data received from server::  ", fm)

        data = fm.split(' ')

        hostname = data[0]
        state = data[2]

        if (state == 'NS'):
            print("[C]: Could not find match in RS Table. Looking in TS")

            if (hostname != ts_hostname):
                ts_hostname = hostname
                hostname_bool = 0
                ts_hostname = hostname

                sa_sameas_myaddress =mysoc.gethostbyname(ts_hostname)

            # connect to the server on local machine

                server_binding_ts=(sa_sameas_myaddress,ts_port)

                ts.connect(server_binding_ts)

                tsFlow(ts, x, f, f1)
            else:
                hostname_bool = 1
                tsFlow(ts, x, f, f1)
        else :
            #writing to file
            f1.write(fm)
            f1.write('\n')

    f.close()
    f1.close()


    cs.close()

    print("[C]: Closed connection to server")

    exit()


def tsFlow (ts, x, f, f1):

    print("[C]: Sending message ", x)
    #sending to server
    ts.send(x.encode())
    print("[C]: Message sent")

    #recieving from server
    data_from_server=ts.recv(100)

    fm = str(data_from_server.decode('utf-8'))

    print("[C]: Data received from server::  ", fm)

    f1.write(fm)
    f1.write('\n')

    #ts.close()

    #print("[C]: Closed connection to server")

t2 = threading.Thread(name='client', target=client)

t2.start()
