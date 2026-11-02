import socket

port = 5050
buffer = 16
format = "utf-8"

hostname = socket.gethostname()
server_ip_address = socket.gethostbyname(hostname)
server_soc_address = (server_ip_address, port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_soc_address)
server.listen()
print("Server is listening on IP: {}, PORT: {}".format(server_ip_address, port))

while True:
    conn, client_soc_address = server.accept()
    print("Accepted connection from (client): {}".format(client_soc_address))
    connected = True
    while connected:
        initial_msg = conn.recv(buffer).decode(format)
        print("Upcoming message length: {}".format(initial_msg))
        
        if initial_msg:
            msg_length = int(initial_msg)
            msg = conn.recv(msg_length).decode(format)
            print("Received message: {}".format(msg))
            if msg == "Terminated":
                connected = False
                conn.send("Connection terminated by server.".encode(format))
                print("Closing connection with (client): {}".format(client_soc_address))
            else:
                conn.send("Message received.".encode(format))
                print("Acknowledged receipt of message from (client): {}".format(client_soc_address))
                print("Received message from client: {}".format(msg))
    conn.close()