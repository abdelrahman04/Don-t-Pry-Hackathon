import socket
import sys

# Function to send data to a specific port
def send_data(port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Set a timeout for the socket
        client_socket.settimeout(15)  # Timeout set to 10 seconds
        try:
            # Connect to the server
            client_socket.connect(('192.168.25.235', port))
            # Send the data
            client_socket.sendall(data.encode('utf-8'))
            print(f"Sent data to port {port}: {data}")
            print(sys.argv[4])
            print("taba3t")
            if sys.argv[4] == '10':
                print("ayhaga python.py")
                while True:
                    try:
                        received_data = client_socket.recv(1024).decode('utf-8')
                        if received_data:
                            print(f"{received_data}")
                            break
                    except socket.timeout:
                        print("No response from server, timed out.")
                        break
        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    port = 9000

    the_args = [sys.argv[1], sys.argv[2], sys.argv[3]]

    data_to_send = '.'.join(the_args)

    print(data_to_send)

    send_data(port, data_to_send)

if __name__ == "__main__":
    main()
