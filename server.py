import sys, socket

def gtMessage(server, messages, address):
        if len(messages) == 0:
            server.sendto(b"", address)
            return
        message = "\n".join(messages)
        server.sendto(message.encode(), address)
        

def main(argv):
    host = ""
    port = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    save_clients = {}
    messages = {}

    while True:
        data, address = server.recvfrom(1024)
        decoded = data.decode("utf-8")
        if len(decoded) > 1:
            number, deco = decoded.split(" ", 1)
        else:
            number = decoded
        # print(decoded)
        if number[0] == "1":
            # print(save_clients)
            joined_string = ", ".join(save_clients.values())
            server.sendto(joined_string.encode(), address)
            for name in save_clients.values():
                messages[name].append(deco + " has joined")
            save_clients[address] = deco
            messages[deco] = []
        elif number[0] == "2":
            for name in save_clients.values():
                if name != save_clients[address]:
                    messages[name].append(save_clients[address] + ": " + deco)
            gtMessage(server, messages[save_clients[address]], address)
            messages[save_clients[address]] = []
        elif number[0] == "3":
            old_name = save_clients[address]
            save_clients[address] = deco
            messages[deco] = messages[old_name]
            messages.pop(old_name)
            gtMessage(server, messages[save_clients[address]], address)
            messages[save_clients[address]] = []

            for name in save_clients.values():
                if name != save_clients[address]:
                    messages[name].append(old_name + " changed his name to " + deco)
        #    print(messages, save_clients)
        elif number[0] == "4":
            messages.pop(save_clients[address])
            left = save_clients[address]
            save_clients.pop(address)
            for name in save_clients.values():
                messages[name].append(left + " has left the group")
            server.sendto(b"leave", address)
        elif number[0] == "5":
            gtMessage(server, messages[save_clients[address]], address)
            messages[save_clients[address]] = []
        else:
            server.sendto(b"Illegal request", address)

if __name__ == "__main__":
    main(sys.argv[1:])
