import socket

port = 5050
buffer = 16
format = "utf-8"

hostname = socket.gethostname()
server_ip_address = socket.gethostbyname(hostname)
client_ip_address = socket.gethostbyname(hostname)
server_soc_address = (server_ip_address, port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_soc_address)
print("Connected to server on IP: {}, PORT: {}".format(server_ip_address, port))

# Client is ready to send and receive messages

def sending_encoded_message(msg):
    message = msg.encode(format)  # "Hello"
    msg_length = len(message) # 5
    send_len = str(msg_length).encode(format) # "5"
    send_len += b' ' * (buffer - len(send_len)) # "5           "
    client.send(send_len)
    client.send(message)
    
    sent_from_server = client.recv(2048).decode(format)
    print("Sent from server: {}".format(sent_from_server))

sending_encoded_message("40")
sending_encoded_message("45")
sending_encoded_message("Terminated")
