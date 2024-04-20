import socket


def tcp_echo_server():
    #create a socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind the socket
    server_address = '127.0.0.1'
    server_port = 54321
    server_sock.bind((server_address, server_port))

    #listen for incoming connections
    server_sock.listen(5)

    print("Server is listening for incoming connections")

    try:
        while True:
            #accept connections
            client_sock, client_address = server_sock.accept()

            try:
                #send and receive data
                message = client_sock.recv(1024)
                #send response back to client
                response = f"UP {server_address} {server_port}"
                client_sock.sendall(response.encode())
            
            finally:
                #close client connection
                    client_sock.close()
    except KeyboardInterrupt:
        print("Server is shutting down")
    
    finally:
        #Close server socket
        server_sock.close()
        print("Server socket closed")

if __name__ == "__main__":
    tcp_echo_server()