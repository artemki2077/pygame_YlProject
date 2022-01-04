import threading
import socket


def listen(conn, addr):
    try:
        while 1:
            date = conn.recv(1024).decode("utf-8")
            if date != "":
                x, y = list(map(float, date.split(", ")))[:2]
                users[addr] = (x, y)
                conn.sendall(str(users).encode("utf-8"))
                # for i in users:
                #     conn.sendto(ppp, i)
                print(users)
    except:
        listen(conn, addr)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 9999)
sock.bind(server_address)
sock.listen(5)

users = {}

while 1:
    connection, client_address = sock.accept()
    # connection.sendto()
    print(f"connect: {client_address}")
    users[client_address] = (0, 0)
    threading.Thread(target=listen, args=(connection, client_address, )).start()
