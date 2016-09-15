import socket
from .help_utils import *
if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 8081))
    sock.listen(5)
    conn, addr = sock.accept()
    try:
        while 1: # работаем постоянно
            conn, addr = sock.accept()
            print("New connection from " + addr[0])
            try:
                parse(conn, addr)
            except:
                senderror(conn, 404)
            finally:
                # так при любой ошибке
                # сокет закроем корректно
                conn.close()
    finally: sock.close()
