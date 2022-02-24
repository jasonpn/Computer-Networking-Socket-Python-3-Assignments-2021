#TESTED ON PYTHON 2.7

from socket import *


msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
#Fill in start
mailserver = ("comp3203.ca", 2525) #Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
#Fill in end
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
clientSocket.send("MAIL FROM: <test@cmail.carleton.ca> \r\n".encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
clientSocket.send("RCPT TO: <abdou@comp3203.ca> \r\n".encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Fill in end

# Send DATA command and print server response.
# Fill in start
clientSocket.send("DATA\r\n".encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
print('send msg')
if recv1[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send message data.
# Fill in start
clientSocket.send("SUBJECT: test\r\n".encode())
clientSocket.send(msg.encode())

# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
print('end msg')
if recv1[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.send("QUIT\r\n".encode())
print("quit")
clientSocket.close()
# Fill in end
