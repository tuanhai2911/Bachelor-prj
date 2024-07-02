import socket
import time

# UDP settings
UDP_IP = "0.0.0.0"
UDP_PORT = 1234

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Variables for calculating sampling rate
start_time = time.time()
sample_count = 0

try:
    while True:
        # Receive data from UDP socket
        data, addr = sock.recvfrom(1024)
        # Print received data
        print("Received data:", data.decode())
        
        # Increment sample count
        sample_count += 1
        
        # Check if 10 seconds have elapsed
        if time.time() - start_time >= 10:
            break
        
    # Calculate sampling rate
    sampling_rate = sample_count / (time.time() - start_time)
    print("Sampling rate:", sampling_rate, "samples per second")
    # Reset variables
    start_time = time.time()
    sample_count = 0
            
finally:
    sock.close()
