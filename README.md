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