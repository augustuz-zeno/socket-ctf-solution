import socket

host = "127.0.0.1"
port = 9009

url = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url.settimeout(0.5)
url.connect((host, port))
print("Подключено к серверу!")

def recv_until_prompt():
    buffer = b''
    codes = None
    while True:
        try:
            data = url.recv(1024)
            if not data:
                break
            buffer += data
            text = buffer.decode()
            print(text, end='')
            if "[>] ASCII kodlar:" in text:
                lines = text.splitlines()
                for line in reversed(lines):
                    if "[>] ASCII kodlar:" in line:
                        codes = line.split("[>] ASCII kodlar:")[1].strip()
                        return codes
        except socket.timeout:
            continue
    return codes

word_from_server = recv_until_prompt()

if word_from_server:
    decoded_text = ''.join(chr(int(x)) for x in word_from_server.split())
    print(f"\nОтправляю код: {decoded_text}")
    url.send((decoded_text + "\n").encode())

try:
    while True:
        data = url.recv(1024)
        if not data:
            break
        print(data.decode(), end='')
except socket.timeout:
    pass

url.close()