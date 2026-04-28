import socket
import re

host = "127.0.0.1"
port = 9003

url = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url.settimeout(1)
url.connect((host, port))
print("Подключено к серверу!")

def recv_all():
    data = b''
    while True:
        try:
            part = url.recv(1024)
            if not part:
                break
            data += part
        except socket.timeout:
            break
    return data.decode()

def solve_math(text):
    for line in text.splitlines():
        if "Savol" in line:
            part = line.split("Savol:")[-1]
            match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', part)
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

for _ in range(3):
    text = recv_all()
    print(text)
    answer = solve_math(text)
    print("Ответ:", answer)
    if answer:
        url.send((answer + "\n").encode())

print(recv_all())

url.close()