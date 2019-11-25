import time
from C_ClientSocket import ClientSocket

if __name__ == "__main__" :
    while True:
        try :
            ClientSocket.run_client()
        except ConnectionRefusedError:
            # Connection Refused
            # Update for Every 2 seconds
            time.sleep(2)
            pass
        # TODO: Keep worflow in while loop after the task
        if (task done) :
            break
    while True :
        pass
