import socket
import time

# Completati cu adresa IP a platformei ESP32
PEER_IP = "192.168.89.20"
PEER_PORT = 10001

MESSAGE1 = b"GPIO4=0"
MESSAGE2 = b"GPIO4=1"
i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    try:
        sock.sendto(MESSAGE1, (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", MESSAGE1)
        time.sleep(3)

        sock.sendto(MESSAGE2, (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", MESSAGE2)
        time.sleep(3)

    except KeyboardInterrupt:
        break