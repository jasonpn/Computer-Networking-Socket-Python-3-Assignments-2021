#TESTED WITH PYTHON 2.7 WITH UDPPINGERSERVER.PY

from socket import *
import time

mailserver = ("", 12000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for pings in range (1, 11):
    msg = ("Ping " + str(pings)+ " " + str(time.time()))
    start = time.time()

    try:
        clientSocket.sendto(msg, mailserver)
        print("PING SENT")
        recv1 = clientSocket.recv(1024).decode()
        print(recv1)
        end = time.time()
        rtt = end - start
        print("RTT = " + str(rtt) + "\n\n")
    except timeout:
        print("Request timed out")

clientSocket.close()
