import socket    
import threading


HOST = '127.0.0.1'
PORT = 5679  # BETWEEN 0 TO 65535 
LISTENER_LIMIT = 5 

# List of all currently connected users  
active_clients = []

# Function to listen for upcoming messages from client
def listen_for_messages_from_client(Client_Socket, username):
    while True:
        try:
            message = Client_Socket.recv(2048).decode('utf-8')
            if message != '':
                final_msg = username + '~' + message
                send_messages_to_all(final_msg)
            else:
                print(f"Message sent from client {username} is empty")
        except Exception as e:
            print(f"Error: {e}")
            break  # Exit the loop on error

def send_message_to_client(Client_socket, message):
    Client_socket.sendall(message.encode())             

# Function to send any new message to all the clients that are currently connected to server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(Client_Socket):
    # Server will listen for client message that will contain the username
    while True:
        username = Client_Socket.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, Client_Socket))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Username is empty")

    threading.Thread(target=listen_for_messages_from_client, args=(Client_Socket, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))  # Binding server to this address and port
        print(f"Running the server host{HOST} port{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")

    server.listen(LISTENER_LIMIT)

    while True:
        # Wait for an incoming connection
        Client_Socket, Client_address = server.accept()
        print(f"Successfully connected to client {Client_address[0], Client_address[1]}")
        threading.Thread(target=client_handler, args=(Client_Socket,)).start()  # Fixed indentation

if __name__ == '__main__':
    main()
