import sys, socket
#send the message to the given client.
#send an empty message if no messages exists
def gtMessage(server, messages, address):
        if messages:
            server.sendto(("\n".join(messages)).encode(), address)
            return
        server.sendto(b"", address)
#checks if the port is in the legall intarval (from the lecture)
def legall_port(port):
    return port > 0 and port <= 2**16

# checks if the key exists in the dictionary
def exist(key,dict):
    return key in dict

# this method is to append messages belongs to other clients
def fill_meassge(clients,messages,message,except_name):
    for name in clients.values():
        if name != except_name:
            messages[name].append(message)

def main(argv):
    host = ""
    port = int(sys.argv[1])
    #here we open a network socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #checking if the port is legall if not we close it
    if not legall_port(port):
        print("illegal port")
        server.close()
    #here we bind the tuple (host,port)
    server.bind((host, port))
    clients = {}
    messages = {}

    while True:
        #here we recive 1024 bit of data from clients
        data, address = server.recvfrom(1024)
        command = data.decode("utf-8")
        if len(command) > 1:
            number, command_string = command.split(" ", 1)
        else:
            number = command
        
        if number[0] == "1" and not exist(address,clients) and len(command_string)!=0:
            server.sendto((", ".join(clients.values())).encode(), address)
            fill_meassge(clients,messages,command_string + " has joined",command_string)
            clients[address] = command_string
            messages[command_string] = []
        elif number[0] == "2" and exist(address,clients):
            fill_meassge(clients,messages,clients[address] + ": " + command_string,clients[address])
            gtMessage(server, messages[clients[address]], address)
            messages[clients[address]] = []
        elif number[0] == "3" and exist(address,clients) :
            old_name = clients[address]
            clients[address] = command_string
            messages[command_string] = messages[old_name]
            messages.pop(old_name)
            gtMessage(server, messages[clients[address]], address)
            messages[clients[address]] = []
            fill_meassge(clients,messages,old_name + " changed his name to " + command_string,clients[address])
        elif number[0] == "4" and exist(address,clients):
            messages.pop(clients[address])
            left = clients[address]
            clients.pop(address)
            fill_meassge(clients,messages,left + " has left the group",left)
            server.sendto(b"leave", address)
        elif number[0] == "5" and exist(address,clients):
            gtMessage(server, messages[clients[address]], address)
            messages[clients[address]] = []
        else:
            server.sendto(b"Illegal request", address)

if __name__ == "__main__":
    main(sys.argv[1:])
