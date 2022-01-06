import threading
import socket
import time


def listen(conn, addr):
    global catcher
    try:
        while 1:
            date = conn.recv(1024).decode("utf-8")
            if date != "":
                x, y = list(map(float, date.split(", ")))[:2]
                users[addr][0] = (x, y)
                conn.sendall(str(users).encode("utf-8"))
                # for i in users:
                #     conn.sendto(ppp, i)
                # print(users)
    except:
        listen(conn, addr)


def is_cross(a, b):
    if a[0] < b[0]:
        ax1, ay1, ax2, ay2 = a[0], a[1], a[0] + 24, a[1] + 24
        bx1, by1, bx2, by2 = b[0], b[1], b[0] + 24, b[1] + 24
    else:
        ax1, ay1, ax2, ay2 = b[0], b[1], b[0] + 24, b[1] + 24
        bx1, by1, bx2, by2 = a[0], a[1], a[0] + 24, a[1] + 24
    xA = [ax1, ax2]
    xB = [bx1, bx2]

    yA = [ay1, ay2]
    yB = [by1, by2]

    if max(xA) < min(xB) or max(yA) < min(yB) or min(yA) > max(yB):
        return False

    elif max(xA) > min(xB) > min(xA):
        return True
    else:
        return True


def check_game():
    global catcher
    while 1:
        # print(users)
        if catcher is not None:
            for i in users.copy():
                if i != catcher:
                    if is_cross(users[catcher][0], users[i][0]):
                        users[catcher][1] = False
                        users[i][1] = True
                        catcher = i
                        time.sleep(5)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 10001)
sock.bind(server_address)
sock.listen(5)

catcher = None
users = {}
threading.Thread(target=check_game).start()
while 1:
    connection, client_address = sock.accept()
    # connection.sendto()
    print(f"connect: {client_address}")
    if len(users) == 0:
        # print(1)
        users[client_address] = [(0, 0), True]
        threading.Thread(target=listen, args=(connection, client_address)).start()
        catcher = client_address
    else:
        users[client_address] = [(0, 0), False]
        threading.Thread(target=listen, args=(connection, client_address)).start()
