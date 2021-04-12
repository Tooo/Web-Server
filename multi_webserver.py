from socket import *
import os.path
import time
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

THREADS = []

NETWORK_CODES = {
    "200": 'HTTP/1.0 200 OK\n\n',
    "304": 'HTTP/1.0 304 NOT MODIFIED',
    "400": 'HTTP/1.0 400 BAD REQUEST\n\n 400: Bad Request',
    "404": 'HTTP/1.0 404 NOT FOUND\n\n 404: File Not Found',
    "408": 'HTTP/1.0 408 REQUEST TIMED OUT\n\n 408: Request Timed Out'
}


def start_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)
    return server_socket


def is_modified_since(headers, filepath):
    for line in headers:
        if "If-Modified-Since:" in line:
            modified_time = time.strptime(line[19:48], '%a, %d %b %Y %H:%M:%S %Z')
            file_time = time.localtime(os.path.getmtime(filepath))
            if modified_time >= file_time:
                return False
            else:
                return True
    return True


def print_headers(headers):
    for info in headers:
        print(info)


def get_response(client_connection):
    try:
        start_time = time.time()
        request = client_connection.recv(1024).decode()
        end_time = time.time()

        if request[0:3] != 'GET':
            return NETWORK_CODES["400"]

    except:
        return NETWORK_CODES["400"]

    if end_time - start_time > 1:
        return NETWORK_CODES["408"]
    else:
        headers = request.split('\n')
        print_headers(headers)
        filename = headers[0].split()[1]

        if filename == '/':
            filename = '/test.html'
        try:
            filepath = "templates" + filename
            fin = open(filepath)
            content = fin.read()
            fin.close()
            is_modified = is_modified_since(headers, filepath)
            if not is_modified:
                date_string = time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime())
                return NETWORK_CODES["304"] + "\r\nDate: " + date_string + "\r\n\r\n"
            else:
                return NETWORK_CODES["200"] + content

        except FileNotFoundError:
            return NETWORK_CODES["404"]
        except:
            return NETWORK_CODES["400"]

def newTCPServerThread(connection_socket):
    response = get_response(connection_socket);
    connection_socket.sendall(response.encode())
    connection_socket.close()
    #time.sleep(1000000)  # Uncomment to check if multithreading is working properly


def listening(server_socket):
    while True:
        client_connection, client_address = server_socket.accept()
        #print("The new connection was made from: ", client_connection.getpeername())             # Uncomment to check if multithreading is working properly
        newThread = threading.Thread(target=newTCPServerThread, args=[client_connection,])
        newThread.start()
        THREADS.append(newThread)
        #print("The number of threads active is: ", threading.active_count())                     # Uncomment to check if multithreading is working properly


def close_server(server_socket):

    for thread in THREADS:
        thread.join()

    server_socket.close()


def main():
    # Start the Server
    server_socket = start_server()

    # Listen to the Client
    listening(server_socket)

    # Close the Server
    close_server(server_socket)


if __name__ == "__main__":
    main()
