from files.help_utils import *
from socket import *
import threading
import os
import argparse

BUFF = 1024
HOST = '127.0.0.1'
PORT = 80
THREADS = 4
thread_list = []
def handler(serversock,number):
    while 1:
        print('waiting for connection... listening on port', PORT)
        print("start thread %d" % number)
        conn, addr = serversock.accept()
        try:
            parse(conn, addr)
        except Exception :
            conn.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('-p', type=int, help='port of server running')
    parser.add_argument('-t', type=int, help='workers count')
    args = vars(parser.parse_args())
    HOST = args['p'] or HOST
    THREADS = args['t'] or THREADS
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    for i in range(THREADS):
        thread_list.append(threading.Thread(target=handler, args=(serversock, i+1)))
    for t in thread_list:
        t.start()
