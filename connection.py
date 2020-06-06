import socket
import pickle
from core import process_data
from paths import server_port, server_ip

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind((server_ip, server_port)) # в кавычках - IP, второй параметр - порт
serv_sock.listen(10)

while True:
    # Бесконечно обрабатываем входящие подключения
    try: client_sock, client_addr = serv_sock.accept()
    except socket.error:
        pass
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        input = client_sock.recv(1024)
        if not input:
            # Клиент отключился
            break
        print('Received data')
        try:
            output = process_data(pickle.loads(input))
        except AttributeError:
            print('Wrong server command')
        print('Processed data')
        print(output)
        output_pickled = pickle.dumps(output)
        print('Pickled output')
        client_sock.sendall(pickle.dumps(output))
        print('Sent data back')

    client_sock.close()