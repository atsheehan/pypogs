import socket

if __name__ == "__main__":
    PORT = 4485
    MAX = 2000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.connect(("localhost", PORT))
    sock.send("SYN")
    data = sock.recv(MAX)
    if data == "SYN-ACK":
        sock.send("ACK")
    sock.close()