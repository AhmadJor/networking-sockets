from sys import argv
import socket 

def main(argv):

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip = argv[0]
	port = int(argv[1])
	while True:
		string = input()
		s.sendto(string.encode(), (ip, port))
		data, addr = s.recvfrom(1024)
		if data == b'leave':
			s.close()
			break
		if data.decode() != '':
			print(data.decode())
			
if __name__ == "__main__":
    main(argv[1:])
