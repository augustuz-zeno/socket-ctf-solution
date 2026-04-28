import socket
import codecs

host = "127.0.0.1"
port = 9004

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
            if "[>] Shifrlangan so'z:" in text:
                lines = text.splitlines()
                for line in reversed(lines):
                    if "[>] Shifrlangan so'z:" in line:
                        word = line.split("[>] Shifrlangan so'z:")[1].strip()
                        return word
        except socket.timeout:
            continue
    return word

word_from_server = recv_until_prompt()

if word_from_server:
    decoded_word = codecs.decode(word_from_server, 'rot_13')
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