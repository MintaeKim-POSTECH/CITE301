import threading
import socket
import yaml

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

# Shared Objects
# Originally, It sould be encapsulated as a class,
# However this code is for demo purpose, which seems to be Okay...
conn = [None, None]
addr = [None, None]

# Connection Handler
def connection_handler(conn, addr, n, next_line_tok):
	if next_line_tok[1] == "EXIT" :
		data = next_line_tok[1]
	else :
		data = next_line_tok[1] + " " + next_line_tok[2]
	conn.sendall(data.encode())
	recv_info = conn.recv(config["MAX_BUF_SIZE"])
	recv_info = recv_info.decode()
	if (recv_info == "DONE"):
		print ("Instruction Done")
		conn.sendall("Position Data".encode())
		return
	else :
		print ("Wrong recv info")
		print (recv_info)
		conn.sendall("Position Data_ERROR".encode())
		return
def run_server():
	serverSock = socket.socket()
	serverSock.bind((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))
	num = 0
	while True:
		serverSock.listen(config["MAX_ROBOT_CONNECTED"])
		conn[num], addr[num] = serverSock.accept()
		num = num + 1
	sock.close()

if __name__ == '__main__':
	t = threading.Thread(target=run_server)
	t.start()
	while (True):
		nextline = input()
		print (nextline)
		nextline_tok = nextline.split(' ')

		if nextline_tok[0] == '0' :
			if conn[0] == None :
				print ('0 passed')
				pass
			else :
				t = threading.Thread(target=connection_handler, args=(conn[0], addr[0], 0, nextline_tok))
				t.start()
		elif nextline_tok[0] == '1' :
			if conn[1] == None :
				print ('1 passed')
				pass
			else :
				t = threading.Thread(target=connection_handler, args=(conn[1], addr[1], 1, nextline_tok))
				t.start()
