import socket
import threading

clients = []   # list to store active client sockets
lock = threading.Lock()

def handle_client(client_socket, addr, server_name, server_integer):
    global clients
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            client_name, client_num = data.split("|")
            client_num = int(client_num)

            if not (1 <= client_num <= 100):
                print("[SERVER] Invalid number. Disconnecting client.")
                break

            total = client_num + server_integer

            message = (
                f"\n=== Broadcast ===\n"
                f"Client: {client_name}\n"
                f"Server: {server_name}\n"
                f"Client Integer: {client_num}\n"
                f"Server Integer: {server_integer}\n"
                f"Sum: {total}\n"
                f"=================\n"
            )

            print(f"[SERVER] Broadcasting result from {addr}")

            # Send message to all connected clients
            with lock:
                for c in clients:
                    try:
                        c.send(message.encode())
                    except:
                        clients.remove(c)

    finally:
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()


def run_server(host="0.0.0.0", port=6000):
    server_name = "Server of John Q. Smith"
    server_integer = 42

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[SERVER] {server_name} listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SERVER] Connection from {addr}")

        with lock:
            clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr, server_name, server_integer),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    run_server()
