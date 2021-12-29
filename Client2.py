import msvcrt
import sys
import threading
from msvcrt import getch
from socket import *
import struct

UDP_PORT = 13117
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE = 0x2  # for offer


# TODO: close sockets, threads

class Client2:
    def __init__(self):
        self.team_name = "HaYetsiratiyot2"
        self.UDP_client_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.UDP_client_socket.bind(('', UDP_PORT))
        self.server_port_num = 0
        self.server_IP_address = ""

    def looking_for_server(self):
        self.TCP_client_socket = socket(AF_INET, SOCK_STREAM)
        print("Client started, listening for offer requests...")
        while True:  # TODO
            try:
                offer, address = self.UDP_client_socket.recvfrom(BUFFER_SIZE)
                cookie, type, self.server_port_num = struct.unpack('Ibh', offer)
            except:
                continue
            if cookie != MAGIC_COOKIE or type != MESSAGE_TYPE:
                continue
            self.server_IP_address = address[0]
            print("Received offer from " + self.server_IP_address + ", attempting to connect...")
            break

    def connecting_to_a_server(self):
        try:
            self.TCP_client_socket.connect((self.server_IP_address, self.server_port_num))
            name_message = self.team_name + '\n'
            self.TCP_client_socket.send(name_message.encode())
            print("connected")
        except:
            print("except")  # TODO
            return

        print("name sent")

    def get_input(self):
        c = sys.stdin.readline()[0]
        # c = '3'  # TODO: change
        print(c)
        self.TCP_client_socket.send(c.encode())

    def game_mode(self):
        try:
            wlcm_msg = self.TCP_client_socket.recv(BUFFER_SIZE)
            print(wlcm_msg.decode())
            # c= msvcrt.getwch()
            # c = getch().decode('ASCII')
            t1 = threading.Thread(target=self.get_input)
            t1.start()
            # t1.join(10)
            win_msg = self.TCP_client_socket.recv(BUFFER_SIZE)
            print(win_msg.decode())
            self.TCP_client_socket.close()
            print("Server disconnected, listening to offer requests...")
        except:
            print("except")


client = Client2()
while True:
    client.looking_for_server()
    client.connecting_to_a_server()
    client.game_mode()



