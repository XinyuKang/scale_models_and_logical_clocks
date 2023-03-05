from machine import Node
import argparse
import threading

TIMES = 5
SECONDS = 60

def main():
    machines = []
    for i in range(len(port_list)):
        print(f"machie ID {i}")
        machines.append(Node(i, host, port_list[i], port_list))

    # # run the scale model at least 5 times for at least one minute each time
    # print("start running clock cycles")
    # for i in range(TIMES):
    #     for machine in machines:
    #         machine0_thread = threading.Thread(target=machine.cycle_action, args=(SECONDS, i))
    #         machine0_thread.start()
    #         machine1_thread = threading.Thread(target=machine.cycle_action, args=(SECONDS, i))
    #         machine1_thread.start()
    #         machine2_thread = threading.Thread(target=machine.cycle_action, args=(SECONDS, i))
    #         machine2_thread.start()
    #         # cycle_thread = threading.Thread(target=machine.cycle_action, args=(SECONDS, i))  # overwritten only reference to the thread, the thread itself is still running.
    #         # cycle_thread.start()
        



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