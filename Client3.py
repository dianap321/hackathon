from socket import *
import struct
UDP_PORT = 13117
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE = 0x2  # for offer

#TODO: close sockets, threads

class Client3:
    def __init__(self):
        self.team_name = "HaYetsiratiyot3"
        self.UDP_client_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.UDP_client_socket.bind(('', UDP_PORT))
        self.TCP_client_socket = socket(AF_INET, SOCK_STREAM)
        self.server_port_num = 0
        self.server_IP_address = ""


    def looking_for_server(self):
        print("Client started, listening for offer requests...")
        while True: # TODO
            try:
                offer, address = self.UDP_client_socket.recvfrom(BUFFER_SIZE)
            except:
                continue
            cookie, type, self.server_port_num = struct.unpack('Ibh', offer)
            if cookie != MAGIC_COOKIE or type != MESSAGE_TYPE:
                continue
            self.server_IP_address = address[0]
            print("Received offer from " + self.server_IP_address + ", attempting to connect...")
            break

    def connecting_to_a_server(self):
        try:
            self.TCP_client_socket.connect((self.server_IP_address, self.server_port_num))
            print("connected")
        except:
            print("") # TODO
            return
        name_message = self.team_name + '\n'
        self.TCP_client_socket.send(name_message.encode())
        print("name sent")

    def game_mode(self):
        while True:
            print("game")


client = Client3()
client.looking_for_server()
client.connecting_to_a_server()
client.game_mode()



