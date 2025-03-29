import socket
import ssl
import sys

def run_server(choice):
    host = "127.0.0.1"
    port = 65002
    encrypted = True
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    match choice:
        case "0":
            # Plaintext
            encrypted = False
        case "1":
            # SSL 3
            context.maximum_version_version = ssl.TLSVersion.SSLv3
        case "2":
            # TLS 1.1
            context.maximum_version_version = ssl.TLSVersion.TLSv1_1
        case "3":
            # TLS 1.2
            context.maximum_version_version = ssl.TLSVersion.TLSv1_1
        case _:
            context.maximum_version_version = ssl.TLSVersion.MAXIMUM_SUPPORTED
    if encrypted == True:
        # Set up certificates
        context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")
        context.check_hostname = False

        # Set up socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        server_socket.settimeout(20)
        print(f"[Server] Active. Listening to {host} on {port}")
        
        try:
                conn, addr = server_socket.accept()
                print(f"Connection from {addr}")
                
                # Secure the connection with SSL/TLS
                with context.wrap_socket(conn, server_side=True) as secure_conn:
                    data = secure_conn.recv(1024)
                    print(f"Received: {data.decode()}")
                    secure_conn.sendall(b"Hello, secure client!")
                    secure_conn.close()

        except KeyboardInterrupt:
            print("[Server] Could not connect.")
            print("[Server] Server shutting down.")
            server_socket.close()
            quit()

    # Don't wrap securely
    else:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        server_socket.settimeout(20)
        print(f"[Server] Active. Listening to {host} on {port}")
        try:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")
            data = conn.recv(1024)
            print(f"{data.decode()}")
            conn.sendall(b"[Server] Hello client")
            server_socket.close()   
            quit()     
        except socket.timeout:
            print("[Server] Could not connect.")
            print("[Server] Server shutting down.")
            server_socket.close()
            quit()
        except KeyboardInterrupt:
            print("Shutting down")
            server_socket.close()
            quit()

if __name__ == "__main__":
    # This is where we call the function
    choice = sys.argv[1]  # Expected to be passed when launching the subprocess
    run_server(choice)