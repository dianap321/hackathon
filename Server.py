import struct
import time
from random import *
from threading import *
from socket import *
host_name = gethostname() # TODO: change how we get the host
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE = 0x2  # for offer
UDP_PORT = 13117


class Server:
    def __init__(self):
        self.server_port = 2041
        self.IP_address = gethostbyname(host_name)  # TODO: change how we get the host
        self.connections = []
        self.sem = Semaphore(1)
        self.answering_player = ""
        self.player_answer = '10'

        # Set UDP socket
        self.UDP_server_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_server_socket.bind((self.IP_address, 12345))  # TODO: do we need to pass a port num?
        self.UDP_server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # Set TCP socket
        self.TCP_server_socket = socket(AF_INET, SOCK_STREAM)
        self.TCP_server_socket.bind((self.IP_address, self.server_port))




    def send_UDP_offer(self):
        #print("in UDP")
        while len(self.connections) < 2:
           # self.send_UDP_offer()
            #print("in while")
            BROADCAST_PORT = 13117
            packet_format = struct.pack('Ibh', MAGIC_COOKIE, MESSAGE_TYPE, self.server_port) # TODO: last parameter?
            self.UDP_server_socket.sendto(packet_format, ('<broadcast>', BROADCAST_PORT))
            time.sleep(1)

    def connect_2_TCP(self):
        #print("in TCP connect")
        while len(self.connections) < 2:
            try:
                #print("in try")
                clientSocket, address = self.TCP_server_socket.accept()
                team_name = clientSocket.recv(2048).decode()[:-1]
                self.connections.append([team_name, clientSocket, address])
                #print("after")
            except:
                #print("in except")
                #print("") # TODO
                continue
            # print(team_name)

    def waiting_for_clients(self):
        #print("in waiting")
        try:
            self.TCP_server_socket.listen(15)
        except:
            return False
            #print("")
        thread1 = Thread(target=self.send_UDP_offer)
        thread2 = Thread(target=self.connect_2_TCP)
        #print("after thread")
        print("Server started, listening on IP address " + self.IP_address)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        return True

    def communication_with_clients(self, client_identifier, msg):
        reciever_socket = self.connections[client_identifier][1]
        try:
            reciever_socket.send(msg)
            c = reciever_socket.recv(1024).decode()
            #print(c)
            self.sem.acquire()
            # print("111")
            if self.player_answer == '10':
                # print("222")
                self.player_answer = c
                # print("333")
                self.answering_player = self.connections[client_identifier][0]
                # print("444")
            self.sem.release()
            # print("i finished")
        except:
            return
            # print("except")


    def check_answer(self, correct_answer):
        result = "Game over!\nThe correct answer was " + correct_answer + "!\n\n"
        if self.player_answer == '10': # draw
            result += "It's a draw!"
        elif self.player_answer == correct_answer:
            result += "Congratulations to the winner: " + self.answering_player
        else:
            if self.connections[0][0] == self.answering_player:
                result += "Congratulations to the winner: " + self.connections[1][0]
            else:
                result += "Congratulations to the winner: " + self.connections[0][0]
        res_to_send = bytes(result, 'utf-8')
        try:
            for player in self.connections:
                player[1].send(res_to_send)
        except:
            print("Couldn't finish executing the game, trying to connect again...")
        # print("end of check")

    def random_math_question(self):
        answer = randrange(0, 9)
        number_one = randrange(0, 1000)
        operator = choice(['+', '-'])
        number_two = -1
        if operator == '+':
            number_two = answer - number_one
        elif operator == '-':
            number_two = number_one - answer
        question = "" + str(number_one) + operator + str(number_two)
        return question, str(answer)

    def game_mode(self):
        #name_list = self.connections.keys()
        time.sleep(3)  # TODO: change to 10
        question, answer = self.random_math_question()
        msg = "Welcome to Quick Maths.\nPlayer 1: " + self.connections[0][0] + "\nPlayer 2: " + self.connections[1][0] + "\n==\nPlease answer the following question as fast as you can:\nHow much is " + question + "?\n"
        msg_to_send = bytes(msg, 'utf-8')
        t_c1 = Thread(target=self.communication_with_clients, args=(0, msg_to_send,))
        t_c2 = Thread(target=self.communication_with_clients, args=(1, msg_to_send,))
        t_c1.start()
        t_c2.start()
        t_c1.join(5)
        t_c2.join(5)
        self.check_answer(answer)  #TODO: change to random answer
        for player in self.connections:
            try:
                player[1].close()
            except:
                pass
                #print("except")
        self.connections.clear()
        self.answering_player = ""
        self.player_answer = '10'
        print("Game over, sending out offer requests...")

#note1
server = Server()
while True:
    is_ready = server.waiting_for_clients()
    if is_ready:
        server.game_mode()
