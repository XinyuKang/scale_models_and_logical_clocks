from machine import Node
import argparse

TIME = 120

def main():
    machines = []
    for i in range(len(port_list)):
        machines.append(Node(i, host, port_list[i], port_list))

    # run for some time
    for _ in range(TIME):
        for machine in machines:
            machine.cycle_action()



if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    # Use like:
    # python main.py -h "127.0.0.1" -p 5555 6666 7777
    parse.add_argument('-h', dest='host', nargs='?', default='127.0.0.1')
    parse.add_argument('-p', dest='port_list', nargs=3, default=[5555, 6666, 7777], help='List exactly three ports')
    args = parse.parse_args()
    host = args.host
    port_list = args.port_list
    main()