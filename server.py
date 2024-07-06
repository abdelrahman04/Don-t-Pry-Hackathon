import os
import socket
import threading
import time

# Define the ports to listen on
ports = [9000, 9001, 9002, 9003, 9004, 9005]

# Dictionary to hold flags for each port
port_flags = {port: False for port in ports}

# Function to handle incoming data on a specific port
def handle_connection(port):
    global port_flags
    
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the port
        server_socket.bind(('0.0.0.0', port))
        # Listen for incoming connections
        server_socket.listen()
        
        print(f"Listening on port {port}...")
        
        # Accept incoming connections
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            
            # Read the data received from the client
            data = client_socket.recv(1024).decode('utf-8').strip()
            if data:
                print(f"Received data on port {port}: {data}")
                
                # Extract x and y values from data
                x, y = data.split(',')
                
                # Construct file path based on port number
                file_path = f"Player-Data/Input-P{ports.index(port)}-0"
                
                
                # Write data to file in the required format
                with open(file_path, 'w') as file:
                    file.write(f"{x} {y}\n")
                    print(f"Data written to {file_path}")
                
                # Set flag to True when data is received
                port_flags[port] = True
            
            # Close the client socket
            client_socket.close()

# Function to check if all ports have received data and run OS commands if true
def check_and_run_commands():
    global port_flags
    
    while True:
        if all(port_flags[port] for port in ports):
            # Run your first OS command (change directory)
            print("All ports have received data. Running OS command 1...")
            os.system("cd /Users/momenashraf/Desktop/mp-spdz-0.3.8/")
            
            # Run your second OS command (start mascot-party.x instances)
            print("Running OS command 2...")
            os.system("for i in {0..5}; do ./mascot-party.x $i DontPry-V1.0 -pn 12171 -h localhost -N 6 & done; wait")

            # Reset all flags to False
            port_flags = {port: False for port in ports}
            
        # Adjust sleep time as needed to reduce CPU usage in the loop
        time.sleep(1)

# Create a thread for each port to handle incoming data
threads = []
for port in ports:
    thread = threading.Thread(target=handle_connection, args=(port,))
    thread.start()
    threads.append(thread)

# Create a separate thread to check and run OS commands
check_thread = threading.Thread(target=check_and_run_commands)
check_thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Wait for the check thread to complete
check_thread.join()

