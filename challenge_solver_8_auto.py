import socket
import re

host = "127.0.0.1"
port = 9008

url = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url.settimeout(1)
url.connect((host, port))
print("Подключено к серверу!")

def recv_until_prompt():
    data = b''
    while True:
        try:
            part = url.recv(1024)
            if not part:
                break
            data += part
            if b">>>" in data:
                break
        except socket.timeout:
            break
    return data.decode(errors="ignore")

def solve_math(text):
    for line in text.splitlines():
        if "=" in line:
            match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)\s*=', line)
            if match:
                a, op, b = match.groups()
                a, b = int(a), int(b)
                print("Найдено:", a, op, b)
                if op == '+':
                    return str(a + b)
                elif op == '-':
                    return str(a - b)
                elif op == '*':
                    return str(a * b)
                elif op == '/':
                    return str(a // b)
    return None

for _ in range(5):
    text = recv_until_prompt()
    print(text)
    answer = solve_math(text)
    print("Ответ:", answer)
    if answer:
        url.send((answer + "\n").encode())

print(recv_until_prompt())

url.close()