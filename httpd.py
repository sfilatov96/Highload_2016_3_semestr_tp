from files.help_utils import *
from socket import *
import os
import argparse

BUFF = 1024
HOST = '127.0.0.1'
PORT = 80
WORKERS_COUNT = 2
NCPU = 2
forks = []


def handler(serversock, pid, ROOT_DIR):
    while 1:
        print('waiting for connection... listening on port', PORT)
        conn, addr = serversock.accept()
        try:
            parse(conn, addr, pid, ROOT_DIR)
        except Exception:
            conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('-p', type=int, help='port of server running')
    parser.add_argument('-r', type=str, help='root document')
    parser.add_argument('-n', type=str, help='number of CPU')
    args = vars(parser.parse_args())
    HOST = args['p'] or HOST
    NCPU = args['n'] or NCPU
    ROOT_DIR = args['r'] or ""
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    for x in range(0, WORKERS_COUNT * NCPU):
        pid = os.fork()
        forks.append(pid)
        if pid == 0:
            print('PID:', os.getpid())
            handler(serversock, os.getpid(), ROOT_DIR)
    serversock.close()

    for pid in forks:
        os.waitpid(pid, 0)
