# reverse-shell
A simple reverse shell client/server program to connect more than 1 machines (client) to another machine (server). The server sends CLI commands while the client/s receive and execute it whenever applicable.

## How does it work?

###### reverse_shell_client.py
This is the client program. It connects to a scoket that's using the hardcoded server IP address. After connection, it waits and receives command from the server and executes it.

###### reverse_shell_multiclient_server.py
This is the multiple-client server program. It's a multi-threaded program with 2 threads: 1) A thread that handles the socket connections 2) A thread that service that socket connections. The user can send CLI commands to selected clients and receives reply through shell ('turtle>').
Commands:
    1. turtle> list
        List all connections available
    2. turtle> select [num]
        Select target [num] to send commands
        After the target is selected, we can no send CLI commands to the client such as 'echo Hello there!' or 'mkdir testing_folder', etc.
    3. turtle> quit 
        Go back to turtle>

###### reverse_shell_single_server.py
This is the single-client server program. It only accepts one client a time.

## How to use it?

1. Modify line 5 of reverse_shell_client.py to add actual server IP address where ***_server.py will be ran. Note that this may need to be modified whenever the server IP address is changed. Another option is to run the server program on a remote server that has static IP address.
2. Copy the reverse_shell_multiclient_server.py to all the client machines. 
3. Run the reverse_shell_multiclient_server.py to start listening to connections.
4. Run the reverse_shell_client.py on all the client machines to start multiple connections.
5. On the server machine, the user can now start typing CLI commands to send to selected client machine.
