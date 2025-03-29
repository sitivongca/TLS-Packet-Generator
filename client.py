import socket
import ssl
import sys

def run_client(choice):
    host = "localhost"
    port = 65002
    encrypted = True

    match choice:
        case "0":
            # Plaintext
            encrypted = False
        case "1":
            # SSL 2/3
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        case "2":
            # TLS 1.1
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        case "3":
            # TLS 1.2
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        case _:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

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