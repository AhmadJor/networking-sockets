import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True :
    string = input()
    s.sendto(string.encode(), ('127.0.0.1', 12345))
    data, addr = s.recvfrom(1024)
    if data == b'leave':
        s.close()
        break
    if data.decode() != '':
        print(data.decode())
    
#s.close()