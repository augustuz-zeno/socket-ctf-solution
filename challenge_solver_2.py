import socket

host = "127.0.0.1"
port = 9002

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
            if "[>] So'z:" in text:
                lines = text.splitlines()
                for line in reversed(lines):
                    if "[>] So'z:" in line:
                        word = line.split("[>] So'z:")[1].strip()
                        return word
        except socket.timeout:
            continue
    return word

word_from_server = recv_until_prompt()

if word_from_server:
    mirrored_word = word_from_server[::-1]
    print(f"\nОтправляем зеркальное: {mirrored_word}")
    url.send((mirrored_word + "\n").encode())

try:
    while True:
        data = url.recv(1024)
        if not data:
            break
        print(data.decode(), end='')
except socket.timeout:
    pass

url.close()