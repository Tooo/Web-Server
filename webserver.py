from socket import *
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

def get_response(client_connection):
    try:
        start_time = time.time()
        request = client_connection.recv(1048576).decode()
        end_time = time.time()
        print(request)

        if(request[0:3] != 'GET'):
            return 'HTTP/1.0 400 BAD REQUEST\n\n 400: Bad Request'

        #print(start_time, end_time, end_time-start_time)
    except:
        return 'HTTP/1.0 400 BAD REQUEST\n\n 400: Bad Request'

    if end_time - start_time > 1:
        return 'HTTP/1.0 408 REQUEST TIMED OUT\n\n 408: Request Timed Out' 
    else:
        headers = request.split('\n')
        filename = headers[0].split()[1]
        if filename == '/':
            filename = '/test.html'
        try:
            fin = open("templates"+filename)
            content = fin.read()
            fin.close()
            return 'HTTP/1.0 200 OK\n\n' + content
        except FileNotFoundError:
            return 'HTTP/1.0 404 NOT FOUND\n\n 404: File Not Found'
        except:
            return 'HTTP/1.0 400 BAD REQUEST\n\n 400: Bad Request'

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    client_connection, client_address = server_socket.accept()
    response = get_response(client_connection)
    client_connection.sendall(response.encode())
    client_connection.close()


server_socket.close()