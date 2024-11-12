import socket
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
UDP_PORT = 5001

# TCP connection
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect((TCP_IP, TCP_PORT))

# UDP connection
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive_tcp():
    """Receives TCP messages from the server."""
    while True:
        try:
            msg = tcp_client.recv(1024).decode()
            if msg:
                print(f"TCP message: {msg}")
        except:
            break

def receive_udp():
    """Receives UDP messages from the server."""
    while True:
        try:
            msg, _ = udp_client.recvfrom(1024)
            print(f"UDP message: {msg.decode()}")
        except:
            break

# Start threads to listen for TCP and UDP messages
threading.Thread(target=receive_tcp, daemon=True).start()
threading.Thread(target=receive_udp, daemon=True).start()

# Sending messages
try:
    while True:
        msg = input("Enter message:  ")
        if msg.startswith('udp:'):
            udp_client.sendto(msg[4:].encode(), (TCP_IP, UDP_PORT))
        else:
            tcp_client.send(msg.encode())
except KeyboardInterrupt:
    print("Client exiting.")
finally:
    tcp_client.close()
    udp_client.close()
