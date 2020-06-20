import socket
import pickle
from paths import server_ip, server_port


def server_conn(command, data_to_send=None, verbose=False):
    if verbose:
        print('Starting command')
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if verbose:
        print('Created socket')
    client_sock.connect((server_ip, server_port))
    if verbose:
        print('Connected to socket')
    data_source = [command, data_to_send]
    data_string = pickle.dumps(data_source)
    client_sock.sendall(data_string)
    if verbose:
        print('Data sent')

    data_received = []
    while True:
        packet = client_sock.recv(1024)
        data_received.append(packet)
        if not packet:
            break


    if verbose:
        print('Data received')
    client_sock.close()
    if verbose:
        print('Socket closed')
    data_unpickled = pickle.loads(b"".join(data_received))
    return data_unpickled