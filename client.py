import socket

# Define the ports to connect to
ports = [9000, 9001, 9002, 9003, 9004, 9005]

# Data to send to each port
data_to_send = [f"{i},{i}" for i in range(len(ports))]


# Function to send data to a specific port
def send_data(port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect(('192.168.22.235', port))

        # Send the data
        client_socket.sendall(data.encode('utf-8'))

        print(f"Sent data to port {port}: {data}")


# Send data to each port
for port, data in zip(ports, data_to_send):
    send_data(port, data)
