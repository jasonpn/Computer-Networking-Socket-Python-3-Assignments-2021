#TESTED ON PYTHON 2.7

from socket import *
import sys
import traceback

if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
serverPort = 6789

tcpSerSock.bind(("", serverPort))

tcpSerSock.listen(1)
# Fill in end.

while 1:
        # Strat receiving data from the client
        print('Ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from:', addr)
        # Read a message from the client
        fromClient = tcpCliSock.recv(1024)
        print("\nHTTP Request Received:\n"+fromClient)
        if (fromClient.split(" ")[0] != "GET"):
             print("Not supported")
             tcpCliSock.send("HTTP/1.0 501 Not Implemented\r\nConnection: close\r\n\r\n".encode())
             tcpCliSock.close()
             continue

        URL = fromClient.split(" ")[1]
        print("URL: "+URL)
        # Extract the file and host names from the given URL
        URLSize = len(URL.split("/"))
        filename = URL.split("/")[URLSize-1]
        if filename == "":
            filename="index.html"
        if URLSize > 2:
            hostname = URL.split("/")[2]
        else:
            hostname = URL.split("/")[0]
        print("File name: "+filename)
        print("Host: "+hostname)

        try:
                # Check wether the file exist in the cache
                fileobj = open(filename)
                # ProxyServer finds a cache hit
                objectFound = "true"
                print('Read from cache')
        # Error handling for file not found in cache
        except IOError:
                # Create a socket on the proxyserver to the main server
                c = socket(AF_INET, SOCK_STREAM)
                try:
                      # Connect to the socket on port 80
                      # Fill in start.
                      c.connect((hostname, 80))
                      # Fill in end.
                      print('Connected to server')
                      request = "GET /" + filename + " HTTP/1.0\r\nHost: " + hostname + "\r\nContent-Type:text/html;charset=UTF-8\r\n\r\n"
                      c.send(request.encode())
                      print('Sent a GET request')
                      response = c.recv(1024000)
                      # Now write response to a local file
                      print('Obtained file from server')
                      fileobj = open(filename,'wb')
                      # Response contains both: HTTP response headers and data
                      fileobj.write(response.decode().split("\r\n\r\n")[1].encode())
                      fileobj.close()
                      fileobj = open(filename)
                      objectFound = "true"
                except:
                      print("File not found on the server, or unable to cache file locally")
                      objectFound = "false"
                      # HTTP response message to client for file not found
                      # Fill in start.
                      tcpCliSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                      tcpCliSock.send("404 NOT FOUND")
                      tcpCliSock.close()
                      # Fill in end.

        if objectFound == "true":
                # Read fileobj from memory
                filecontent = fileobj.read()
                tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
                tcpCliSock.send("Content-Type:text/html\r\nConnection: close\r\n".encode())
                # Now send the cached file to the client
                # Fill in start.
                tcpCliSock.send(filecontent)
                # Fill in end.
                tcpCliSock.send("\r\n".encode())

        # Close the client and the server sockets
        # Fill in start.
        tcpCliSock.close()
        # Fill in end.
tcpSerSock.close()
