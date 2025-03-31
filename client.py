import ssl_loader
ssl_loader.load_openssl()
import socket
from OpenSSL import SSL
import sys

def run_client(choice):
    host = "localhost"
    port = 65002
    encrypted = True
    context = SSL.Context(SSL.SSLv23_METHOD)

    match choice:
        case "0":
            encrypted = False
        case "1":
            # SSL 3
            context.set_options(SSL.OP_NO_TLSv1 | SSL.OP_NO_TLSv1_1 | SSL.OP_NO_TLSv1_2 | SSL.OP_NO_TLSv1_3)
            context.set_cipher_list(b"ALL")
            context.load_verify_locations("certs/ca/insecureCA.crt")
        case "2":
            context.set_options(SSL.OP_NO_TLSv1_1 | SSL.OP_NO_TLSv1_2 | SSL.OP_NO_TLSv1_3)
            context.set_cipher_list(b"ALL")
            context.load_verify_locations("certs/ca/insecureCA.crt")
        case "3":
            # TLS 1.1
            context.set_options(SSL.OP_NO_TLSv1_2 | SSL.OP_NO_SSLv3)
            context.set_cipher_list(b"ALL")
            context.load_verify_locations("certs/ca/insecureCA.crt")
        case "4":
            # TLS 1.2
            context.set_options(SSL.OP_NO_TLSv1_3)
            context.load_verify_locations("certs/ca/ca.crt")
        case _:
            # TLS 1.3
            context.load_verify_locations("certs/ca/ca.crt")
            pass

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    if encrypted:
        # Create an SSL connection on top of the socket
        connection = SSL.Connection(context, client_socket)
        connection.set_tlsext_host_name(host.encode())  # Set server hostname for SNI
        connection.set_connect_state()

        # Perform the handshake
        connection.do_handshake()

        # Send and receive data
        connection.send(b"Hello, secure server!")
        data = connection.recv(1024)
        print(f"[Server]: {data.decode()}")

        connection.close()
    else:
        client_socket.send(b"[Client] Hello sent from client")
        data = client_socket.recv(1024)
        print(f"{data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    choice = sys.argv[1]
    run_client(choice)
