import socket
import threading

def listen_for_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

def run_client(server_ip="127.0.0.1", port=6000):
    client_name = "Client of John Q. Smith"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Start background thread to listen for broadcasts
    threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True).start()

    while True:
        try:
            client_num = int(input("Enter an integer (1–100, 0 to quit): "))
        except ValueError:
            print("Invalid input")
            continue

        if client_num == 0:
            break

        message = f"{client_name}|{client_num}"
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    run_client()
