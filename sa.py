import logging
import socket
import threading
import random
import time
import os
import datetime

import argparse


class LogicalClock:
    def __init__(self, initial_time=0):
        self.time = initial_time
        self.lock = threading.Lock()
        
    def add(self):
        with self.lock:
            self.time += 1

    def update(self, other):
        with self.lock:
            self.time = max(self.time, other) + 1

    def get_time(self):
        with self.lock:
            return self.time
        
class Node():
    def __init__(self, id, host, port, port_list):
        # clear up the logger if previously used
        if os.path.isfile(str(port)+".log"):
            os.remove(str(port)+".log")
        # setup the logger (loguru failed on multi threads)
        # self.logger = logger.bind(instance_id=id)
        # self.logger.configure(handlers=[{"sink": str(port)+".log", "format": "{time} {extra[instance_id]} {message}"}])
        # try logging instead
        self.set_log(str(port)+".log","logger_" + str(port))
        # setup the logical clock
        self.logical_clock = LogicalClock()
        # setup the clock cycle
        self.clock_cycle = random.randint(1, 6)
        # log clock cycle and machine ID to the logger
        self.logger.info(f"Machine {id} has clock cycle {self.clock_cycle}")
        # set up all nodes
        self.port_list = port_list
        self.id = id   # machine id, used in action
        self.host = host
        self.port = port
        # set up listener for the machine
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.message_queue = []
        # begin listening for messages
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def set_log(self, filename, logger_name):
        handler = logging.FileHandler(filename)
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO) 
        self.logger.addHandler(handler)


    def listen(self):
        self.server.listen(10)
        #print('Listening...')
        try:
            while True:
                client, addr = self.server.accept()
                #print(f"Connected with {str(addr)}")
                t = threading.Thread(target=self.receive, args=(client,))
                t.start()

        except Exception as e:
            print('Server Error Occurred: ', e)
            print("stop the server")
            self.server.close()


    def receive(self, client):
        #print('Receiving...')
        try:
            while True:
                data = client.recv(1024).decode("ascii")
                if data!="":
                    self.message_queue.append(data)
                
        except Exception as e:
            print('Client Error Occurred: ', e)
            print("stop the client")
            if client:
                client.close()

    def cycle_action(self, seconds, run):
        # actions done in given number of seconds, and one clock cycle per second
        # log the clock cycle
        self.logger.info(f"----------------------- Machine {self.id} is starting its {run+1}th run of {seconds} seconds -----------------------") 
        for i in range(seconds):
            start_time = time.time()
            for _ in range(self.clock_cycle):
                # if there is a message in the message queue,
                if len(self.message_queue) != 0:
                    # take one message off the queue, and write in the log
                    message = self.message_queue.pop(0)
                    print(message.split("-")[-1][33:-1])
                    self.logical_clock.update(int(message.split("-")[-1][33:-1]))
                    self.logger.info(
                        f"RECEIVED: {message} - GLOBAL TIME: {i} - LOGICAL CLOCK TIME: {self.logical_clock.get_time()} - MESSAGE QUEUE LEN: {len(self.message_queue)}")

                else:
                    # update the local logical clock,
                    self.logical_clock.add()
                    # generate a random number in the range of 1-10
                    rand = random.randint(1, 10)
                    message = f"'Machine {self.id} has logical clock time {self.logical_clock.get_time()}'"
                    receiver_id_1 = (self.id+1) % 3
                    receiver_id_2 = (self.id+2) % 3
                    if rand == 1:
                        self.send(self.port_list[receiver_id_1], message)
                        # update the log with the send
                        self.logger.info(
                            f"SENT(rand=1): {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {i} - LOGICAL CLOCK TIME: {self.logical_clock.get_time()}")
                    elif rand == 2:
                        self.send(self.port_list[receiver_id_2], message)
                        # update the log with the send
                        self.logger.info(
                            f"SENT(rand=2): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {i} - LOGICAL CLOCK TIME: {self.logical_clock.get_time()}")
                    elif rand == 3:
                        # send message to both machines
                        self.send(self.port_list[receiver_id_1], message)
                        self.send(self.port_list[receiver_id_2], message)
                        # update the log with the send
                        self.logger.info(
                            f"SENT(rand=3): {message} TO MACHINE #{receiver_id_1} and #{receiver_id_2} - GLOBAL TIME: {i} - LOGICAL CLOCK TIME: {self.logical_clock.get_time()}")
                    else:
                        # log the internal event
                        self.logger.info(
                            f"INTERNAL EVENT - GLOBAL TIME: {i} - LOGICAL CLOCK TIME: {self.logical_clock.get_time()}")
  
            # sleep for sometime to make sure that each clock cycle runs for exactly 1 (real world) second   
            time.sleep(1.0 - (time.time() - start_time))
            




    def send(self, port, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, port))   # assume all nodes have the same host
        client.send(message.encode("ascii"))


TIMES = 1
SECONDS = 10

def main():
    machines = []
    for i in range(len(port_list)):
        print(f"machie ID {i}")
        machines.append(Node(i, host, port_list[i], port_list))

    # run the scale model at least 5 times for at least one minute each time
    print("start running clock cycles")
    for i in range(TIMES):
        for machine in machines:
            cycle_thread = threading.Thread(target=machine.cycle_action, args=(SECONDS, i))  # overwritten only reference to the thread, the thread itself is still running.
            cycle_thread.start()

            # Process(target = machine.cycle_action, args = (SECONDS, i)).start()
        

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    # Use like:
    # python main.py -host "127.0.0.1" -ports 5555 6666 7777
    parse.add_argument('-host', dest='host', nargs='?', default='127.0.0.1')
    parse.add_argument('-ports', dest='port_list', nargs=3, default=[5555, 6666, 7777], help='List exactly three ports')
    args = parse.parse_args()
    host = args.host
    port_list = args.port_list
    main()