import ssl_loader
ssl_loader.load_openssl()
import socket
from OpenSSL import SSL
import sys

def run_server(choice):
    host = "127.0.0.1"
    port = 65002
    encrypted = True
    context = SSL.Context(SSL.SSLv23_METHOD)

    match choice:
        case "0":
            encrypted = False
        case "1":
            # SSL 3
            context.set_options(SSL.OP_NO_TLSv1 | SSL.OP_NO_TLSv1_1 | SSL.OP_NO_TLSv1_2 | SSL.OP_NO_TLSv1_3)
            context.use_certificate_file("certs/insecureServer.crt")
            context.load_verify_locations("certs/ca/insecureCA.crt")
        case "2":
            context.set_options(SSL.OP_NO_TLSv1_1 | SSL.OP_NO_TLSv1_2 | SSL.OP_NO_TLSv1_3)
            context.use_certificate_file("certs/insecureServer.crt")
            context.load_verify_locations("certs/ca/insecureCA.crt")
        case "3":
            # TLS 1.1
            context.set_options(SSL.OP_NO_TLSv1_2 | SSL.OP_NO_SSLv3 | SSL.OP_NO_TLSv1_3)
            context.use_certificate_file("certs/insecureServer.crt")
            context.load_verify_locations("certs/ca/insecureCA.crt")
        case "4":
            # TLS 1.2
            context.set_options(SSL.OP_NO_TLSv1_3)
            context.use_certificate_file("certs/server.crt")
            context.load_verify_locations("certs/ca/ca.crt")
        case _:
            # TLS 1.3
            context.use_certificate_file("certs/server.crt")
            context.load_verify_locations("certs/ca/ca.crt")
            pass

    # Set up the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.settimeout(20)
    print(f"[Server] Active. Listening to {host} on {port}")

    if encrypted:
        # Load server certificate and private key
        context.use_privatekey_file("certs/server.key")

        # Set the verification mode to verify peer certificates
        context.set_verify(SSL.VERIFY_NONE, callback=None)

        try:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Secure the connection with SSL/TLS
            secure_conn = SSL.Connection(context, conn)
            secure_conn.set_accept_state()

            secure_conn.do_handshake()

            version = secure_conn.get_protocol_version_name()
            cipher = secure_conn.get_cipher_name()
            print(f"Using: {version} with cipher: {cipher}")

            data = secure_conn.recv(1024)
            print(f"[Client] {data.decode()}")
            secure_conn.sendall(b"Hello, client!")
            secure_conn.close()

        except KeyboardInterrupt:
            print("[Server] Server shutting down.")
            server_socket.close()
            quit()

    else:
        try:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")
            data = conn.recv(1024)
            print(f"{data.decode()}")
            conn.sendall(b"[Server] Hello client")
            conn.close()
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
    choice = sys.argv[1]
    run_server(choice)
