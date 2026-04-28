import socket
import base64

host = "127.0.0.1"
port = 9005

url = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url.settimeout(0.5)
url.connect((host, port))
print("Подключено к серверу!")

def recv_until_prompt():
    buffer = b''
    word = None
    while True:
        try:
            data = url.recv(1024)
            if not data:
                break
            buffer += data
            text = buffer.decode()
            print(text, end='')
            if "[>] Base64:" in text:
                lines = text.splitlines()
                for line in reversed(lines):
                    if "[>] Base64:" in line:
                        word = line.split("[>] Base64:")[1].strip()
                        return word
        except socket.timeout:
            continue
    return word

word_from_server = recv_until_prompt()

if word_from_server:
    decoded_word = base64.b64decode(word_from_server).decode()
    print(f"\nОтправляю декодированное сообщение: {decoded_word}")
    url.send((decoded_word + "\n").encode())

try:
    while True:
        data = url.recv(1024)
        if not data:
            break
        print(data.decode(), end='')
except socket.timeout:
    pass

url.close()