# SSL/TLS Packet Generator

Communicates between client and server through python to use for packet analysis
From SSLv3 to TLSv1.3

![Terminal](/public/example.png)
![Wireshark](/public/SSL3SS.png)

### Dependencies

- Tested with Python 3.10.x
- Tested with OpenSSL 3.0.16
- InquirerPy
- pyca/Cryptography

1. Setup python venv
2. [Install Dependencies](/docs/compiling-guide.md)
3. Run Activate.ps1
4. Run python tlsAnalyzer.py
5. Use Wireshark to capture packets on Adapter for Loopback using filter tcp.port == 65002

### Installation Help

- OpenSSL has to be compiled from source in order to use versions below TLSv1.2
- Cryptography and PyOpenSSL has to be compiled through --no-binary to generate a wheel linked to your own OpenSSL install and not use the precompiled wheel
- Compiling OpenSSL and Cryptography can take a minute
- If there is a space in the path don't forget to use quotes
