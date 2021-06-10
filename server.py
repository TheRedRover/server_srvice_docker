import socket
import sys
import time
import os
# EYE_SERVICE_PORT=5555
# KUBERNETES_SERVICE_HOST=10.43.0.1
# CLIENT_SERVICE_HOST=10.43.198.238
# CLIENT_SERVICE_PORT=5554
# KUBERNETES_SERVICE_PORT=443
# KUBERNETES_SERVICE_PORT_HTTPS=443
# EYE_SERVICE_HOST=10.43.73.77
def log(data: str):
    with open("data.txt", mode="a") as f:
        f.write(f"{data}\n")


server_host = "0.0.0.0"
server_port = None
client_host = None
client_port = None
L = 0
while True:
    try:
        server_port = os.environ["SERVER_SERVICE_PORT"]
        client_host = os.environ["CLIENT_SERVICE_HOST"]
        client_port = os.environ["CLIENT_SERVICE_PORT"]
        break
    except KeyError:
        log(f"Try env #{L}")
        L += 1
        time.sleep(5)

log(f"Got SERVER_HOST is {server_host}")
log(f"Got SERVER_PORT is {server_port}")
log(f"Got CLIENT_HOST is {client_host}")
log(f"Got CLIENT_PORT is {client_port}")

self_address = (server_host, int(server_port))

remote_address = (client_host, int(client_port))


N = 0

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(self_address)
    except Exception as e:
        log(str(e))
        while True:
            pass
    sock.listen(10)
    conn, addr = sock.accept()  # blocking
    data = conn.recv(512)
    log(data.decode())
    conn.close()
    sock.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    while True:
        try:
            sock.connect(remote_address)
            break
        except Exception as e:
            pass
    sock.sendall(f"Ping #{N}".encode())
    sock.shutdown(socket.SHUT_WR)
    sock.close()

    N += 1
    time.sleep(5)
