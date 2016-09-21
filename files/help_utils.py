from os.path import splitext, getsize
import urllib.request
from time import gmtime, strftime
errors = {
    403: "errors/403_error.html",
    404: "errors/404_error.html",
    405: "errors/405_error.html",
    500: "errors/500_error.html",
}
status = {
    200: "200 OK",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    500: "500 Internal Server Error"
}
types = {
    ".js": "application/javascript",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".html": "text/html",
    ".png": "image/png",
    ".gif": "image/gif",
    ".css": "text/css",
    ".txt": "text/plain",
    ".swf": "application/x-shockwave-flash",
}


def senderror(conn, code):
    address = errors[code]
    filetype = splitext(address)[1]
    f = open(address, "rb")
    status = code
    all_data = getsize(address)
    typ = types[filetype]
    send_answer(conn, status, all_data, typ)
    while True:
        data = f.read()
        if not data: break
        conn.sendall(data)

    f.close()
    conn.close()


def sendfile(conn, file, method, ROOT_DIR):
    address = urllib.request.unquote(file)
    address = address.split("?")[0]
    address = (ROOT_DIR or '.') + address
    filetype = splitext(address)[1]
    if '..' in address:
        senderror(conn, 404)
    else:
        try:
            f = open(address, "rb")
            status = 200
            all_data = getsize(address)
            typ = types[filetype]
            send_answer(conn, status, all_data, typ)
            if method != "HEAD":
                while True:
                    data = f.read()
                    if not data:
                        break
                    conn.sendall(data)

                f.close()
            conn.close()
        except FileNotFoundError:
            if "index.html" in address:
                senderror(conn, 403)
            else:
                senderror(conn, 404)
        except IsADirectoryError:
            if file[-1] == '/':
                file += "index.html"
            else:
                file += "/index.html"
            sendfile(conn, file, method, ROOT_DIR)


def parse(conn, addr, pid, ROOT_DIR):
    data = b""
    print("send on PID: ", pid)
    while not b"\r\n" in data:  # ждём первую строку
        tmp = conn.recv(1024)
        if not tmp:  # сокет закрыли, пустой объект
            break
        else:
            data += tmp

    if not data:  # данные не пришли
        return  # не обрабатываем

    udata = data.decode("utf-8")
    udata = udata.split("\r\n", 1)[0]
    print(udata.split(" ", 2))
    if len(udata.split(" ", 2)) < 3:
        senderror(conn, 404)
    else:
        method, address, protocol = udata.split(" ", 2)
        if method in ("GET", "HEAD"):
            sendfile(conn, address, method, ROOT_DIR)
        else:
            senderror(conn, 405)


def send_answer(conn, i, length, typ):
    conn.send(b"HTTP/1.1 " + status[i].encode("utf-8") + b"\r\n")
    conn.send(b"Date: " + '{date}'.format(date=strftime("%a, %d %b %Y %X GMT", gmtime())).encode("utf-8") + b"\r\n")
    conn.send(b"Server: sfilatov96\r\n")
    conn.send(b"Connection: keep-alive\r\n")
    conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
    conn.send(b"Content-Length: " + str(length).encode("utf-8") + b"\r\n")
    conn.send(b"\r\n")
