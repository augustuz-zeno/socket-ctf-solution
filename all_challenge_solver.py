import socket
import re
import codecs
import base64

HOST = "127.0.0.1"

def get_data(s, stop_trigger=None):
    data = ""
    while True:
        try:
            part = s.recv(4096).decode(errors="ignore")
            if not part: break
            data += part
            print(part, end="")
            if stop_trigger and stop_trigger in data: break
        except socket.timeout:
            break
    return data

def talk(port, marker=None, processor=None, send_first=None, stop_trigger=None, manual_payload=None):
    print(f"\n--- Challenge {port % 100} ---")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        s.connect((HOST, port))
        if send_first: 
            s.send(f"{send_first}\n".encode())
        text = get_data(s, stop_trigger)
        if manual_payload:
            s.send(f"{manual_payload}\n".encode())
            get_data(s)
        elif marker and marker in text and processor:
            ans = processor(text)
            if ans:
                s.send(f"{ans}\n".encode())
                get_data(s)

def solve_math_v3(text):
    match = re.search(r'Savol:\s*(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)', text)
    if match:
        a, op, b = match.groups()
        if op == '+': return str(int(a) + int(b))
        if op == '-': return str(int(a) - int(b))
        if op == '*': return str(int(a) * int(b))
        if op == '/': return str(int(a) // int(b))
    return None

def solve_math_v8(text):
    match = re.search(r'(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)\s*=', text)
    if match:
        a, op, b = match.groups()
        if op == '+': return str(int(a) + int(b))
        if op == '-': return str(int(a) - int(b))
        if op == '*': return str(int(a) * int(b))
        if op == '/': return str(int(a) // int(b))
    return None

talk(9001, send_first="HELLO")
talk(9002, "So'z:", lambda t: re.search(r"So'z:\s*(\w+)", t).group(1)[::-1])

print("\n--- Challenge 3 ---")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(0.8)
    s.connect((HOST, 9003))
    for _ in range(3):
        txt = get_data(s)
        ans = solve_math_v3(txt)
        if ans: s.send(f"{ans}\n".encode())
    print(get_data(s))

talk(9004, "so'z:", lambda t: codecs.decode(re.search(r"so'z:\s*(\w+)", t).group(1), 'rot_13'))
talk(9005, "Base64:", lambda t: base64.b64decode(re.search(r"Base64:\s*([\w=]+)", t).group(1)).decode())

talk(9006, stop_trigger=">>>", manual_payload="py7h0n")

def solve_caesar(text):
    s_m = re.search(r"(?:Shift|miqdori):\s*(\d+)", text)
    w_m = re.search(r"so'z:\s*(\w+)", text)
    if not (s_m and w_m): return ""
    shift, word, res = int(s_m.group(1)), w_m.group(1), ""
    for c in word:
        if c.isalpha():
            start = ord('a') if c.islower() else ord('A')
            res += chr((ord(c) - start - shift) % 26 + start)
        else: res += c
    return res
talk(9007, "so'z:", solve_caesar)

print("\n--- Challenge 8 ---")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(0.8)
    s.connect((HOST, 9008))
    for _ in range(5):
        txt = get_data(s, stop_trigger=">>>")
        ans = solve_math_v8(txt)
        if ans: s.send(f"{ans}\n".encode())
    print(get_data(s))

talk(9009, "kodlar:", lambda t: "".join(chr(int(x)) for x in re.search(r"kodlar:\s*([\d\s]+)", t).group(1).split()), stop_trigger=">>>")