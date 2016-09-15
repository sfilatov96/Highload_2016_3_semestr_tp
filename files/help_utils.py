from os.path import splitext,getsize
errors = {
    404: "errors/404_error.html",
    405: "errors/405_error.html",
    500: "errors/500_error.html"
}
status = {
    200: "200 OK",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    505: "500 Internal Server Error"
}
types = {
    ".js": "application/javascript",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpg",
    ".html": "text/html",
    ".png": "image/png",
    ".gif": "image/gif",
    ".css": "text/css",
    ".txt": "text/plain",
    ".swf": "application/swf",

}
def senderror(conn, code):
    address = errors[code]
    filetype = splitext(address)[1]
    f = open(address, "rb")
    status = code
    all_data = getsize(address)
    print(all_data)
    typ = types[filetype]
    send_answer(conn, status,all_data,typ)
    while True:
            data = f.read()
            if not data: break
            conn.sendall(data)

    f.close()


def sendfile(conn, file):
    address = file
    filetype = splitext(address)[1]
    try:
        f = open(address, "rb")
        status=200
        all_data = getsize(address)
        print(all_data)
        typ = types[filetype]
        send_answer(conn, status,all_data,typ)

        while True:
                data = f.read()
                if not data: break
                conn.sendall(data)

        f.close()
    except FileNotFoundError:
        senderror(conn,404)


def parse_addr(conn, addr):
    if addr[-1] == "/":
        addr = addr + "index.html"
        sendfile(conn,addr)
    else:
        sendfile(conn,addr)


def parse(conn, addr):

    data = b""

    while not b"\r\n" in data: # ждём первую строку
        tmp = conn.recv(1024)
        if not tmp:   # сокет закрыли, пустой объект
            break
        else:
            data += tmp

    if not data:      # данные не пришли
        return        # не обрабатываем

    udata = data.decode("utf-8")
    udata = udata.split("\r\n", 1)[0]
    method, address, protocol = udata.split(" ", 2)
    print(method, address, protocol)
    if method in ("GET","HEAD"):
        print(address)
        parse_addr(conn,address)
    else:
        senderror(conn, 405)
    return 0

def send_answer(conn, i, length, typ):
    conn.send(b"HTTP/1.1 " + status[i].encode("utf-8") + b"\r\n")
    conn.send(b"Server: sfilatov96\r\n")
    conn.send(b"Connection: keep-alive\r\n")
    conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
    conn.send(b"Content-Length: " + str(length).encode("utf-8") + b"\r\n")
    conn.send(b"\r\n")