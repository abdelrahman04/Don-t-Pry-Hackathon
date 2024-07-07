
import os
import socket
import threading
import time
import subprocess

# Define the port to listen on
port = 9000

# Dictionary to hold flags for each client
client_flags = {}
client_hashes = {}

# List to hold client connections
client_connections = []

# Lock for synchronizing access to client_connections and counters
connections_lock = threading.Lock()

# Counter to assign unique IDs to clients
client_counter = 0

# Function to handle incoming data from clients
def handle_client(client_socket, client_address):
    global client_flags, client_hashes, client_counter

    try:
        print(f"Connection from {client_address}")

        # Read the data received from the client
        data = client_socket.recv(1024).decode('utf-8').strip()
        if data:
            print(f"Received data from {client_address}: {data}")

            # Extract x, y, and z values from data
            x, y, z = data.split('.')

            with connections_lock:
                # Store the flag and hash for the client
                client_flags[client_address] = True
                client_hashes[client_address] = z
                
                # Assign unique ID to the client
                client_id = client_counter
                client_counter += 1

            # Construct file path based on the client ID
            file_path = f"Player-Data/Input-P{client_id}-0"

            # Write data to file in the required format
            with open(file_path, 'w') as file:
                file.write(f"{x} {y}\n")
                print(f"Data written to {file_path}")

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        with connections_lock:
            client_connections.append(client_socket)

# Function to accept incoming connections
def accept_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow address reuse
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the port on all available network interfaces
        server_socket.bind(('0.0.0.0', port))
        # Listen for incoming connections
        server_socket.listen()

        print(f"Listening on port {port}...")

        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

# Function to periodically run OS commands and broadcast results
def periodic_command_runner():
    global client_flags, client_hashes, client_counter

    while True:
        time.sleep(15)  # Wait for 10 seconds

        with connections_lock:
            if client_flags:
                # Change directory
                os.chdir("/Users/momenashraf/Desktop/mp-spdz-0.3.8/")

                # Run mascot-party.x instances and capture output
                print("Running OS command...")
                process = subprocess.Popen(
                    "for i in {0..5}; do ./mascot-party.x $i DontPry-V1.0 -pn 12171 -h localhost -N 6 & done; wait",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = process.communicate()

                # Filter and find the winner's information
                winner_line = ""
                winner_hash = ""
                output_lines = stdout.decode('utf-8').split('\n')
                for line in output_lines:
                    if "The closest individual is" in line:
                        winner_line = line
                        print(line)
                        break

                # Extract the winner's client address from the output line
                if winner_line:
                    winner_index = int(winner_line.split()[-1])
                    winner_address = list(client_flags.keys())[winner_index]
                    winner_hash = client_hashes[winner_address]
                    broadcast_message = f"Hash: {winner_hash}"

                    # Broadcast the winner's information to all clients
                    for conn in client_connections:
                        try:
                            conn.sendall(broadcast_message.encode('utf-8'))
                        except OSError as e:
                            print(f"Failed to send data to a client: {e}")
                            with connections_lock:
                                client_connections.remove(conn)
                            conn.close()

                # Reset all flags to False
                client_flags = {}
                client_hashes = {}
                client_connections.clear()
                client_counter = 0

# Start the thread to accept connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Start the thread to run commands periodically
command_runner_thread = threading.Thread(target=periodic_command_runner)
command_runner_thread.start()

# Wait for threads to complete
accept_thread.join()
command_runner_thread.join()
