import socket

host = "127.0.0.1"
port = 9008

url = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url.settimeout(0.5)
url.connect((host, port))
print("Подключено к серверу!")

def show_message():
    full_data = b''
    while True:
        try:
            data = url.recv(1024)
            if not data:
                break
            full_data += data
        except socket.timeout:
            break
    print(full_data.decode())

show_message()

for i in range(5):
    show_message()
    message = input(">>> ")
    url.send((message + "\n").encode())
    show_message()

url.close()