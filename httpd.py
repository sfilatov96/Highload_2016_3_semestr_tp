import socket
from files.help_utils import *
if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 8081))
    sock.listen(5)
    conn, addr = sock.accept()
    parse(conn, addr)
    conn.close()
    sock.close()