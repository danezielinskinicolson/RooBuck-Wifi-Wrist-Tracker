import socketserver
import time
import os
class Handler_TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} sent:".format(self.client_address[0]))
        print(self.data)

        with open('ESP_1Log.txt','a') as f:
#            filedata.append(time.strftime('%X %x %Z'))
            f.write(time.strftime('%X %x %Z') +  "   " +  str(self.data) + "\n")
        # just send back ACK for data arrival confirmation
        #self.request.sendall("RD".encode())

if __name__ == "__main__":
    HOST, PORT = "192.168.0.9", 8007

    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    print("Server in operation")
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()