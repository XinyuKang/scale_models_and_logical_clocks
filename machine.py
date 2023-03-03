# we use he loguru library for the logging: https://github.com/Delgan/loguru
from loguru import logger
import socket
import threading
import random
import time

class Node():
    def __init__(self, id, host, port, port_list):
        # setup the logger
        self.logger = logger.add(host+".log", enqueue=True)
        # setup the logical clock
        self.logical_clock = 0
        # setup the clock cycle
        self.clock_cycle = random.randint(1, 6)
        # set up all nodes
        self.port_list = port_list   # make a copy otherwise change in place
        self.id = id   # machine id, used in action
        self.host = host
        self.port = port
        # set up listener for the machine
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.message_queue = []
        # begin listening for messages
        self.listen()

    def listen(self):
        try:
            while True:
                client, addr = self.server.accept()
                print(f"Connected with {str(addr)}")
                t = threading.Thread(target=self.receive, args=(client,))
                t.start()

        except Exception as e:
            print('Server Error Occurred: ', e)
            print("stop the server")
            self.server.close()


    def receive(self, client):
        try:
            while True:
                data = client.recv(1024).decode("ascii")
                self.message_queue.append(data)
                
        except Exception as e:
            print('Client Error Occurred: ', e)
            print("stop the client")
            if client:
                client.close()

    def cycle_action(self):
        # actions done in a clock cycle
        for _ in range(self.clock_cycle):
            # update the local logical clock, 
            self.logical_clock += 1
            # if there is a message in the message queue, 
            if len(self.message_queue) != 0:
                # take one message off the queue, and write in the log
                self.logger.info(f"RECEIVED: {self.pop(0)} - GLOBAL TIME: {time.time()} - LOGICAL CLOCK TIME: {self.logical_clock} - MESSAGE QUEUE LEN: {len(self.message_queue)}")
                
            else:
                # generate a random number in the range of 1-10
                rand = random.randint(1, 10)
                message = f"Machine {self.id} has logical clock time {self.logical_clock}"
                receiver_id_1 = (self.id+1) % 3
                receiver_id_2 = (self.id+2) % 3
                if rand==1:
                    self.send(self.port_list[receiver_id_1], message)
                    # update the log with the send
                    self.logger.info(f"SENT: {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {time.time()} - LOGICAL CLOCK TIME: {self.logical_clock}")
                elif rand==2:
                    self.send(self.port_list[receiver_id_2], message)
                    # update the log with the send
                    self.logger.info(f"SENT: {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {time.time()} - LOGICAL CLOCK TIME: {self.logical_clock}")
                elif rand==3:
                    # send message to both machines
                    self.send(self.port_list[receiver_id_1], message)
                    self.send(self.port_list[receiver_id_2], message)
                    # update the log with the send
                    self.logger.info(f"SENT: {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {time.time()} - LOGICAL CLOCK TIME: {self.logical_clock}")
                    self.logger.info(f"SENT: {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {time.time()} - LOGICAL CLOCK TIME: {self.logical_clock}")
                else:
                    # log the internal event
                    self.logger.info(f"INTERNAL EVENT - GLOBAL TIME: {time.time()} - LOGICAL CLOCK TIME: {self.logical_clock}")


    def send(self, port, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, port))   # assume all nodes have the same host
        client.send(message.encode("ascii"))