from socket import *
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    client_connection, client_address = server_socket.accept()
    start_time = time.time()
    request = client_connection.recv(1048576).decode()
    end_time = time.time()
    # print(request)
    print(start_time, end_time, end_time-start_time)
    if end_time - start_time > 1:
        response = 'HTTP/1.0 408 REQUEST TIMED OUT\n\nRequest Timed Out' 
    else:
        headers = request.split('\n')
        filename = headers[0].split()[1]
        if filename == '/':
            filename = '/test.html'
        try:
            fin = open("templates"+filename)
            content = fin.read()
            fin.close()
            response = 'HTTP/1.0 200 OK\n\n' + content
        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
        
    client_connection.sendall(response.encode())

    client_connection.close()


server_socket.close()