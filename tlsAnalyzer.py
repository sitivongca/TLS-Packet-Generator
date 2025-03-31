import multiprocessing
import subprocess
import time
import sys
from InquirerPy import inquirer

def startServer(choice):
    subprocess.Popen([sys.executable, "server.py", choice])
def startClient(choice):
    time.sleep(1)
    subprocess.Popen([sys.executable, "client.py", choice])

def main():
    tls_choice = inquirer.select(
        message="Select TLS version:",
        choices=[
            "plaintext",
            "SSLv3",
            "TLSv1",
            "TLSv1.1",
            "TLSv1.2",
            "TLSv1.3",
        ],
        default="plaintext",  # Set default choice (TLS 1.2)
    ).execute()

    tls_mapping = {
        "plaintext": "0",
        "SSLv3":     "1",
        "TLSv1":     "2",
        "TLSv1.1":   "3",
        "TLSv1.2":   "4",
        "TLSv1.3":   "5"
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