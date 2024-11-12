import socket
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
UDP_PORT = 5001

# Set up TCP socket
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((TCP_IP, TCP_PORT))
tcp_server.listen()
clients = []

# Set up UDP socket
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((TCP_IP, UDP_PORT))

def handle_tcp_client(conn, addr):
    """Handles incoming TCP messages from a client."""
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:  # If message is empty, the client has disconnected
                break
            print(f"TCP from {addr}: {msg}")
            broadcast_tcp(msg, conn)
    except:
        pass
    finally:
        conn.close()
        if conn in clients:
            clients.remove(conn)

def broadcast_tcp(msg, sender_conn=None):
    """Send TCP message to all clients. If sender_conn is specified, exclude it."""
    for client in clients:
        if client != sender_conn:  # Avoid sending the message back to the sender if specified
            try:
                client.send(msg.encode())
            except:
                client.close()
                clients.remove(client)

def handle_udp():
    """Continuously listens for UDP messages."""
    while True:
        try:
            msg, addr = udp_server.recvfrom(1024)
            print(f"UDP from {addr}: {msg.decode()}")
            # Broadcast to other clients only
            broadcast_udp(msg, addr)
        except:
            pass

def broadcast_udp(msg, sender_addr=None):
    """Send UDP message to all clients except the sender."""
    for client in clients:
        client_addr = client.getpeername()  # Get the client address for comparison
        if sender_addr is None or client_addr != sender_addr:  # Avoid sending the message back to the sender
            try:
                udp_server.sendto(msg, (client_addr[0], UDP_PORT))
            except:
                pass

def accept_clients():
    """Accepts incoming TCP clients."""
    while True:
        conn, addr = tcp_server.accept()
        print(f"New TCP connection from {addr}")
        clients.append(conn)
        threading.Thread(target=handle_tcp_client, args=(conn, addr), daemon=True).start()

# Server-side messaging loop
def server_send_messages():
    """Allows server to send messages to all clients."""
    while True:
        msg = input("Server message : ")
        if msg.startswith("udp:"):
            broadcast_udp(msg[4:].encode())
        else:
            broadcast_tcp(f"Server: {msg}")

# Start server
print("Server is running...")
threading.Thread(target=accept_clients, daemon=True).start()
threading.Thread(target=handle_udp, daemon=True).start()
threading.Thread(target=server_send_messages, daemon=True).start()

# Keep server running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    tcp_server.close()
    udp_server.close()
