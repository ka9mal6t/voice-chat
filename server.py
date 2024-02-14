import socket
import threading

FORMAT = 'utf-8'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
MAX_CONNECTIONS = 5

clients = []


def handle_client(client_sock, address):
    print(f"Connected with {address}")
    clients.append(client_sock)

    while True:
        try:
            data = client_sock.recv(1024)
            if not data:
                break
            broadcast(data, client_sock)
        except:
            break

    clients.remove(client_sock)
    client_sock.close()


def broadcast(message, sender_sock):
    for client in clients:
        if client != sender_sock:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(MAX_CONNECTIONS)
    print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_sock, address))
        client_handler.start()


start_server()