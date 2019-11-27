import time
from C_ClientSocket import ClientSocket

if __name__ == "__main__" :
    # Keeps worflow in while loop after the task
    while True:
        try :
            ClientSocket.run_client()
        except ConnectionRefusedError:
            # Connection Refused
            # Update for Every 2 seconds
            time.sleep(2)
            print ("Connection Refused")
            continue
        # Broken Pipe, then try re-entry
        except ConnectionResetError:
            time.sleep(2)
            print ("Server Process Terminated")
            continue
        except ConnectionAbortedError:
            time.sleep(2)
            print ("Server Process Aborted")
            continue