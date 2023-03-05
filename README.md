# scale_models_and_logical_clocks

We build a model of a small, asynchronous distributed system which runs on a single machine. But we model multiple machines running at different speeds and build a logical clock for each of the model machines.

## Initialization
Each model machine will run at a clock rate (a random number between 1-6) determined during initialization. This real number is the number of clock ticks per second for the machine (i.e. only that many instructions can be performed by the machine during that time). 

Each model machine also has a network queue in which it will hold incoming messages.

Each of the virtual machines are connected to each of the other virtual machines so that messages can be passed between them.

Each virtual machine opens a file as a log. 

Finally, each machine has a logical clock, which should be updated using the rules for logical clocks.

## Work
On each clock cycle, if there is a message in the message queue for the machine (remember, the queue is not running at the same cycle speed) the virtual machine should take one message off the queue, update the local logical clock, and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.

If there is no message in the queue, the virtual machine should generate a random number in the range of 1-10, and

- if the value is 1, send to one of the other machines a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time
- if the value is 2, send to the other virtual machine a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
- if the value is 3, send to both of the other virtual machines a message that is the logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
- if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.

## Installation & Setup
- Python 3.7+
### Pip
```
pip install loguru
```

## Running the System
To run this toy distributed system., follow these steps:
### Clone the repository to your local machine
```
git clone https://github.com/XinyuKang/wire_protocols.git
```
### Run machines
```
python main.py -host '127.0.0.1'
               -ports 5555 6666 7777
```
Replace the `host` and `ports` with your own desired ones. Note that we have three running machines thus `ports` must be a list of three integers. If no arguments is specified in the running command `python main.py`, then the default host and ports specified above will be used.

## Design Decisions
* We decide to assume for our distributed system that all 3 machines run on the same host with different ports. We do this because: 
  * Simplified Configuration: Having all machines running on tthe same host makes it easier to configure and manage the system. 
  * Lower Latency: Since all the machines are running on the same host, communication between them can be faster and more efficient than if they were on separate hosts.

* We execute each machine for a certain number of clock cycles, corresponding to one second in real time, and then suspend its operation until one second has elapsed.

## Reflection
1. In an asynchronous distributed system where different machines are running at different speeds, the logical clocks of each machine may experience sizeable jumps as they advance relative to other machines. These jumps can be a result of variations in the clock cycle lengths and network latency between machines. As such, the logical clocks of each machine may drift apart in value, even though they started from the same initial value.

2. The length of the message queue can be impacted by differences in timing between the machines. For example, if one machine is running much faster than another, it may send a large number of messages to the slower machine before the slower machine has a chance to process them. This can result in a large backlog of messages in the slower machine's message queue