import socketserver
import time
import os
ESP_tag_counter = 0
class Handler_TCPServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = ""
        while(True):
            values = self.request.recv(1024).strip()
            if len(values) < 1:
                break
            else:
                self.data += str(values)
                print("{} sent:" + str(values))    
        print(self.data)
        nameValue = 'ESP_Log_Calibration.txt'
        with open(nameValue,'a') as f:
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