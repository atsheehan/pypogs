import socket
import sched
import time

connected_players = {}

def process_packet(sock, data, address):
    print "Received a packet from", address, "containing", data

    if data == "SYN":
        connected_players[address] = "SYN-ACK sent"
        sock.sendto("SYN-ACK", address)
    elif data == "ACK":
        connected_players[address] = "ACK-ed"

    print "connected players:", connected_players


if __name__ == "__main__":

    PORT = 4485
    MAX = 2000

    scheduler = sched.scheduler(time.time, time.sleep)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("", PORT))
    while True:
        data, address = sock.recvfrom(MAX)
        process_packet(sock, data, address)
