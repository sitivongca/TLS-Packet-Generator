import multiprocessing
import subprocess
import time
from InquirerPy import inquirer

def startServer(choice):
    subprocess.Popen(["python", "server.py", choice])
def startClient(choice):
    time.sleep(1)
    subprocess.Popen(["python", "client.py", choice])

def main():
    tls_choice = inquirer.select(
        message="Select TLS version:",
        choices=[
            "plaintext",
            "SSL 2/3",
            "TLS 1.1",
            "TLS 1.2",
            "TLS 1.3",
        ],
        default="plaintext",  # Set default choice (TLS 1.2)
    ).execute()

    tls_mapping = {
        "plaintext": "0",
        "SSL 2/3": "1",
        "TLS 1.1": "2",
        "TLS 1.2": "3",
        "TLS 1.3": "4"
    }    

    choice = tls_mapping[tls_choice]

    serverProcess = multiprocessing.Process(target=startClient, args=(choice,))
    clientProcess = multiprocessing.Process(target=startServer, args=(choice,))

    serverProcess.start()
    clientProcess.start()
    
    serverProcess.join()
    clientProcess.join()
    time.sleep(1.5)

if __name__=="__main__":
    main()