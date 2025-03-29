import socket
import ssl
import sys

def run_client(choice):
    host = "localhost"
    port = 65002
    encrypted = True
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    print(f"{ssl.TLSVersion.MINIMUM_SUPPORTED}, {ssl.TLSVersion.MAXIMUM_SUPPORTED}")
    context.minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    if encrypted == True:

        context.load_verify_locations("certs/ca/ca.crt")
        with context.wrap_socket(client_socket, server_hostname=host) as secure_socket:
            secure_socket.send(b"Hello, secure server!")
            data = secure_socket.recv(1024)
            print(f"[Server]: {data.decode()}")
            client_socket.close()
            quit()
    else:
        client_socket.send(b"[Client] Hello sent from client")
        data = client_socket.recv(1024)
        print(f"{data.decode()}")
        client_socket.close()
        quit()

if __name__ == "__main__":
    # This is where we call the function
    choice = sys.argv[1]  # Expected to be passed when launching the subprocess
    run_client(choice)