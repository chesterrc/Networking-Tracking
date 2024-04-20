import socket


#Echo server client
def tcp_echo_client_check(message):
    #create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Specify address
    server_address = '127.0.0.1'
    server_port = 54321

    try:
        #Establish a connection
        sock.connect((server_address, server_port))

        #send and receive data
        sock.sendall(message.encode())
        print(message)
        #receive message
        response = sock.recv(1024)
        server_resp = response.decode()
        
    finally:
        sock.close()
        print(server_resp.split())

if __name__ == "__main__":
    tcp_echo_client_check("sent")