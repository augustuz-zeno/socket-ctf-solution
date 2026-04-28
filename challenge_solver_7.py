import socket

host = "127.0.0.1"
port = 9007

def recv_all(sock):
    buffer = b""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            buffer += data
            text = buffer.decode()
            print(text, end="")
            if ">>>" in text:
                return text
        except socket.timeout:
            continue

def parse_challenge(text):
    shift = None
    word = None
    for line in text.splitlines():
        if "[>] Shift" in line:
            shift = int(line.split(":")[1].strip())

        if "[>] Shifrlangan so'z:" in line:
            word = line.split(":")[1].strip()
    return word, shift

def caesar_decode(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1)
sock.connect((host, port))

print("Подключено к серверу!")

text = recv_all(sock)
word, shift = parse_challenge(text)

print("\nСлово:", word)
print("Shift:", shift)

decoded = caesar_decode(word, shift)
print("Ответ:", decoded)

sock.sendall((decoded + "\n").encode())

try:
    while True:    
        response = sock.recv(1024).decode()
        if not response:
            break
        print(response)
except socket.timeout:
    pass

sock.close()