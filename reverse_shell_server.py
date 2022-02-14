import socket
import sys

global host
global port 
global s 


# create a Socket
def create_socket():
    global host
    global port 
    global s 

    host = ""
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


# establish connection with a client (socket must be listening)
def accept_socket():
    conn, addr = s.accept()
    print("Connection has been established! | IP ", addr[0], " | Port ", addr[1])
    return conn


# send commands to client
def send_commands(conn):
    cmd = input()                               # waits for server user input
    if cmd == 'quit':                           # server user wants to quit the program and the connection
        conn.close()
        s.close()
        sys.exit()
    elif len(str.encode(cmd)) > 0:              # server user wants to send commands to client
        conn.send(str.encode(cmd))              # encode cmd into bytes to be able to send to client
        client_response = str(conn.recv(1024),  # receive response from client
                                'utf-8') 
        print(client_response, end="")          # print to server console


# service socket
def service_socket(conn):
    while True:
        send_commands(conn)
    conn.close()


if __name__ == "__main__":
    print('\n=======\nserver.py\n=======\n')

    create_socket()
    bind_socket()
    conn = accept_socket()
    service_socket(conn)

    