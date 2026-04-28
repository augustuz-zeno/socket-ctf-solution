#!/usr/bin/env python3
"""
=============================================================
  Python Socket CTF Challenges Server
  10 ta turli CTF vazifasi - har biri alohida portda
=============================================================

  PORTLAR:
  Challenge 1  -> 9001  (Salom, HELLO yuborish)
  Challenge 2  -> 9002  (So'zni teskari yuborish)
  Challenge 3  -> 9003  (Matematik savollar x3)
  Challenge 4  -> 9004  (ROT13 dekodlash)
  Challenge 5  -> 9005  (Base64 dekodlash)
  Challenge 6  -> 9006  (Parol topish - iplar orqali)
  Challenge 7  -> 9007  (Sezar shifri)
  Challenge 8  -> 9008  (Matematik marafon x5)
  Challenge 9  -> 9009  (ASCII kodlarini matn ga aylantirish)
  Challenge 10 -> 9010  (Grand Final - ko'p bosqichli)

  Ishga tushirish: python ctf_socket_server.py
=============================================================
"""

import socket
import threading
import base64
import codecs
import random
import time

# ─── Flaglar ────────────────────────────────────────────────
FLAGS = {
    1:  "FLAG{w3lc0m3_t0_s0ck3t_w0rld_2024}",
    2:  "FLAG{r3v3rs3_str1ng_m4st3r_x7k9}",
    3:  "FLAG{m4th_w1z4rd_pr0bl3m_s0lv3r}",
    4:  "FLAG{r0t13_1s_34sy_wh3n_y0u_kn0w}",
    5:  "FLAG{b4s364_d3c0d1ng_sk1ll_unl0ck3d}",
    6:  "FLAG{h1nt_hunt3r_p4ssw0rd_cr4ck3r}",
    7:  "FLAG{c43s4r_c1ph3r_h1st0ry_m4k3r}",
    8:  "FLAG{m4th_m4r4th0n_5_0f_5_p3rf3ct}",
    9:  "FLAG{4sc11_t0_t3xt_wh1sp3r3r_z3r0}",
    10: "FLAG{s0ck3t_gr4nd_m4st3r_f1n4l_b0ss}",
}

# ─── Yordamchi funksiya: xabar yuborish ─────────────────────
def send(conn, msg):
    """Ulanishga satr yuboradi (UTF-8, yangi qator bilan)."""
    conn.sendall((msg + "\n").encode("utf-8"))

def recv(conn):
    """Ulanishdan bir satr qabul qiladi, bo'sh joy va yangi qatorlarni olib tashlaydi."""
    data = b""
    while True:
        chunk = conn.recv(1)
        if not chunk or chunk == b"\n":
            break
        data += chunk
    return data.decode("utf-8").strip()

# ─── Challenge 1: Salom de ──────────────────────────────────
def challenge_1(conn, addr):
    """
    Vazifa: Serverga 'HELLO' so'zini yuboring.
    """
    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 1 - Port 9001")
    send(conn, "  [*] Python Socket CTF Serveriga xush kelibsiz!")
    send(conn, "=" * 50)
    send(conn, "[?] Men bilan gaplashmoqchi bo'lsang, avval salom de.")
    send(conn, "[?] Menga aynan 'HELLO' so'zini yuborishi kerak.")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer == "HELLO":
        send(conn, "[+] Tabriklayman! To'g'ri javob!")
        send(conn, f"[>] FLAG: {FLAGS[1]}")
    else:
        send(conn, f"[-] Noto'g'ri! Sen '{answer}' yubording, men 'HELLO' kutayotgan edim.")

# ─── Challenge 2: Teskari so'z ──────────────────────────────
def challenge_2(conn, addr):
    """
    Vazifa: Server yuborgan so'zni TESKARI yuboring.
    """
    words = ["python", "socket", "network", "hacker", "challenge", "security", "exploit"]
    word = random.choice(words)
    reversed_word = word[::-1]

    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 2 - Port 9002")
    send(conn, "  [*] Teskari So'z Vazifasi")
    send(conn, "=" * 50)
    send(conn, "[?] Men senga bir so'z yuboraman.")
    send(conn, "[?] Sen o'sha so'zni TESKARI holda yuborishingiz kerak.")
    send(conn, f"[>] So'z: {word}")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer.lower() == reversed_word:
        send(conn, "[+] Ajoyib! So'zni teskari yozishni bilasan!")
        send(conn, f"[>] FLAG: {FLAGS[2]}")
    else:
        send(conn, f"[-] Noto'g'ri! '{word}' ning teskarisi '{reversed_word}' edi, sen '{answer}' yubording.")

# ─── Challenge 3: Matematik savollar x3 ─────────────────────
def challenge_3(conn, addr):
    """
    Vazifa: 3 ta matematik savolni ketma-ket to'g'ri javoblang.
    """
    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 3 - Port 9003")
    send(conn, "  [*] Matematik Savollar (3 ta)")
    send(conn, "=" * 50)
    send(conn, "[?] Men senga 3 ta matematik savol beraman.")
    send(conn, "[?] Har birini to'g'ri javoblasan - flagni olasan!")
    send(conn, "-" * 50)

    ops = [
        (lambda a, b: (f"{a} + {b}", a + b)),
        (lambda a, b: (f"{a} * {b}", a * b)),
        (lambda a, b: (f"{a} - {b}", a - b)),
    ]

    for i in range(3):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        question, correct = random.choice(ops)(a, b)
        send(conn, f"[{i+1}/3] Savol: {question} = ?")
        send(conn, ">>> ")
        answer = recv(conn)
        try:
            if int(answer) == correct:
                send(conn, "[+] To'g'ri!")
            else:
                send(conn, f"[-] Noto'g'ri! To'g'ri javob: {correct}")
                send(conn, "[-] Vazifani qayta urinib ko'ring.")
                return
        except ValueError:
            send(conn, "[-] Raqam yuborish kerak edi!")
            return

    send(conn, "[+] Barcha 3 ta savolni to'g'ri javoblading! Matematika ustasi!")
    send(conn, f"[>] FLAG: {FLAGS[3]}")

# ─── Challenge 4: ROT13 ──────────────────────────────────────
def challenge_4(conn, addr):
    """
    Vazifa: ROT13 bilan shifrlangan so'zni dekodlab yuboring.
    """
    secrets = ["sunshine", "keyboard", "terminal", "firewall", "network"]
    secret = random.choice(secrets)
    encoded = codecs.encode(secret, "rot_13")

    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 4 - Port 9004")
    send(conn, "  [*] ROT13 Shifri Vazifasi")
    send(conn, "=" * 50)
    send(conn, "[?] ROT13 shifri - har bir harfni 13 ta oldinga siljitadi.")
    send(conn, "[?] Quyidagi shifrlangan so'zni dekodlab yuboringiz:")
    send(conn, f"[>] Shifrlangan so'z: {encoded}")
    send(conn, "[i] Maslahat: Python'da codecs.decode(text, 'rot_13') ishlatishingiz mumkin.")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer.lower() == secret:
        send(conn, "[+] ROT13 ustasiga aylanding!")
        send(conn, f"[>] FLAG: {FLAGS[4]}")
    else:
        send(conn, f"[-] Noto'g'ri! To'g'ri javob '{secret}' edi.")

# ─── Challenge 5: Base64 dekodlash ──────────────────────────
def challenge_5(conn, addr):
    """
    Vazifa: Base64 encoded so'zni dekodlab yuboring.
    """
    secrets = ["cybersecurity", "pythonrocks", "socketpro", "ctfchamp", "hacktheplanet"]
    secret = random.choice(secrets)
    encoded = base64.b64encode(secret.encode()).decode()

    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 5 - Port 9005")
    send(conn, "  [*] Base64 Dekodlash Vazifasi")
    send(conn, "=" * 50)
    send(conn, "[?] Base64 - ma'lumotni kodlash usuli.")
    send(conn, "[?] Quyidagi Base64 kodlangan so'zni dekodlab yuboringiz:")
    send(conn, f"[>] Base64: {encoded}")
    send(conn, "[i] Maslahat: import base64; base64.b64decode(text).decode()")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer.lower() == secret:
        send(conn, "[+] Base64 dekodlovchisiz!")
        send(conn, f"[>] FLAG: {FLAGS[5]}")
    else:
        send(conn, f"[-] Noto'g'ri! To'g'ri javob '{secret}' edi.")

# ─── Challenge 6: Parol topish ──────────────────────────────
def challenge_6(conn, addr):
    """
    Vazifa: 3 ta ip/maslahat asosida parolni toping.
    Parol: "py7h0n" - iplar beriladi.
    """
    password = "py7h0n"

    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 6 - Port 9006")
    send(conn, "  [*] Maxfiy Parolni Top!")
    send(conn, "=" * 50)
    send(conn, "[?] Men bir maxfiy parolni yashirganman.")
    send(conn, "[?] Senga 3 ta ip beraman - parolni topishing kerak!")
    send(conn, "-" * 50)
    send(conn, "[IP 1] Parol 6 belgidan iborat.")
    send(conn, "[IP 2] U mashhur dasturlash tili nomi, lekin ba'zi harflari raqam bilan almashtirilgan.")
    send(conn, "[IP 3] 'y' oldida 'p', '0' o'rnida 'o', '7' o'rnida biror harf...")
    send(conn, "[IP 4] Ushbu til 1991-yilda Guido van Rossum tomonidan yaratilgan.")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer.lower() == password:
        send(conn, "[+] Parolni topdingiz! Dedektiv ekansiz!")
        send(conn, f"[>] FLAG: {FLAGS[6]}")
    else:
        send(conn, f"[-] Noto'g'ri parol: '{answer}'. Iplarni qayta o'qi.")

# ─── Challenge 7: Sezar shifri ──────────────────────────────
def challenge_7(conn, addr):
    """
    Vazifa: Berilgan shift bilan Sezar shifriga solingan so'zni dekodlab yuboring.
    """
    def caesar_encode(text, shift):
        result = ""
        for ch in text:
            if ch.isalpha():
                base = ord('a') if ch.islower() else ord('A')
                result += chr((ord(ch) - base + shift) % 26 + base)
            else:
                result += ch
        return result

    words = ["hacking", "network", "python", "socket", "cipher"]
    word = random.choice(words)
    shift = random.randint(3, 15)
    encoded = caesar_encode(word, shift)

    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 7 - Port 9007")
    send(conn, "  [*] Sezar Shifri Vazifasi")
    send(conn, "=" * 50)
    send(conn, "[?] Sezar shifri - har bir harfni N ta o'ngga siljitadi.")
    send(conn, f"[>] Shift (siljish) miqdori: {shift}")
    send(conn, f"[>] Shifrlangan so'z: {encoded}")
    send(conn, "[i] Maslahat: Har bir harfni shift miqdorida ORQAGA siljiting.")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer.lower() == word:
        send(conn, "[+] Sezar shifrini sindirdingiz! Julius Sezar xafa bo'ldi...")
        send(conn, f"[>] FLAG: {FLAGS[7]}")
    else:
        send(conn, f"[-] Noto'g'ri! To'g'ri javob '{word}' edi.")

# ─── Challenge 8: Matematik marafon x5 ──────────────────────
def challenge_8(conn, addr):
    """
    Vazifa: 5 ta matematik savolni ketma-ket to'g'ri javoblang.
    Murakkabroq (ko'paytirish, bo'lish, ko'p raqamlar).
    """
    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 8 - Port 9008")
    send(conn, "  [*] Matematik Marafon (5 ta savol)")
    send(conn, "=" * 50)
    send(conn, "[?] 5 ta matematik savolni ketma-ket to'g'ri javoblang!")
    send(conn, "[?] Bitta xato - boshidan boshlash kerak bo'ladi!")
    send(conn, "-" * 50)

    for i in range(5):
        op = random.choice(["+", "-", "*"])
        if op == "*":
            a, b = random.randint(2, 15), random.randint(2, 15)
        else:
            a, b = random.randint(10, 100), random.randint(10, 100)

        if op == "+":
            correct = a + b
        elif op == "-":
            correct = a - b
        else:
            correct = a * b

        send(conn, f"[{i+1}/5] {a} {op} {b} = ?")
        send(conn, ">>> ")
        answer = recv(conn)
        try:
            if int(answer) == correct:
                send(conn, f"[+] To'g'ri! ({i+1}/5)")
            else:
                send(conn, f"[-] Noto'g'ri! To'g'ri javob: {correct}. Boshidan boshlang!")
                return
        except ValueError:
            send(conn, "[-] Faqat raqam yuborish kerak!")
            return

    send(conn, "[+] Matematik marafonni yakunladingiz! 5/5 to'g'ri!")
    send(conn, f"[>] FLAG: {FLAGS[8]}")

# ─── Challenge 9: ASCII kodlari ─────────────────────────────
def challenge_9(conn, addr):
    """
    Vazifa: Bo'sh joy bilan ajratilgan ASCII kodlarini matnga aylantiring.
    """
    words = ["hello", "python", "socket", "cyber", "flag"]
    word = random.choice(words)
    ascii_codes = " ".join(str(ord(c)) for c in word)

    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 9 - Port 9009")
    send(conn, "  [*] ASCII Kodlari Vazifasi")
    send(conn, "=" * 50)
    send(conn, "[?] Quyidagi ASCII raqamlari bir so'zni belgilaydi.")
    send(conn, "[?] Raqamlarni matnga aylantrib yuboringiz.")
    send(conn, f"[>] ASCII kodlar: {ascii_codes}")
    send(conn, "[i] Maslahat: chr(72) -> 'H', ''.join(chr(int(x)) for x in codes.split())")
    send(conn, ">>> ")

    answer = recv(conn)
    if answer.lower() == word:
        send(conn, "[+] ASCII tilini bilasiz!")
        send(conn, f"[>] FLAG: {FLAGS[9]}")
    else:
        send(conn, f"[-] Noto'g'ri! To'g'ri javob '{word}' edi.")

# ─── Challenge 10: Grand Final (Ko'p bosqichli) ─────────────
def challenge_10(conn, addr):
    """
    Vazifa: 4 bosqichli murakkab vazifa - barchasini to'g'ri bajarasang flag!
    """
    send(conn, "=" * 50)
    send(conn, "  CTF Challenge 10 - Port 9010 - GRAND FINAL!")
    send(conn, "  [*] Ko'p Bosqichli Final Vazifa")
    send(conn, "=" * 50)
    send(conn, "[!] Bu oxirgi va eng murakkab vazifa!")
    send(conn, "[?] 4 bosqichni muvaffaqiyatli o'tsang - Grand Master flagini olasan!")
    send(conn, "-" * 50)

    # Bosqich 1: Parol
    send(conn, "[BOSQICH 1] Parol nima? (Maslahat: dasturlash tili + 2024)")
    send(conn, ">>> ")
    ans1 = recv(conn)
    if ans1.lower() != "python2024":
        send(conn, "[-] 1-bosqich xato! Parol: dasturlash_tili + 2024")
        return
    send(conn, "[+] 1-bosqich o'tdi!")

    # Bosqich 2: Math
    a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
    correct2 = a * b + c
    send(conn, f"[BOSQICH 2] Matematik savol: ({a} * {b}) + {c} = ?")
    send(conn, ">>> ")
    ans2 = recv(conn)
    try:
        if int(ans2) != correct2:
            send(conn, f"[-] 2-bosqich xato! To'g'ri javob: {correct2}")
            return
    except ValueError:
        send(conn, "[-] Raqam kerak edi!")
        return
    send(conn, "[+] 2-bosqich o'tdi!")

    # Bosqich 3: Base64
    secret = "grand_master"
    encoded = base64.b64encode(secret.encode()).decode()
    send(conn, f"[BOSQICH 3] Bu Base64 ni dekodla: {encoded}")
    send(conn, ">>> ")
    ans3 = recv(conn)
    if ans3.lower() != secret:
        send(conn, f"[-] 3-bosqich xato! To'g'ri: '{secret}'")
        return
    send(conn, "[+] 3-bosqich o'tdi!")

    # Bosqich 4: Sezar shifri
    def caesar_decode(text, shift):
        result = ""
        for ch in text:
            if ch.isalpha():
                base = ord('a') if ch.islower() else ord('A')
                result += chr((ord(ch) - base - shift) % 26 + base)
            else:
                result += ch
        return result

    final_word = "victory"
    shift = 5
    encoded_final = "".join(
        chr((ord(c) - ord('a') + shift) % 26 + ord('a')) if c.isalpha() else c
        for c in final_word
    )
    send(conn, f"[BOSQICH 4] Sezar shifri (shift={shift}): '{encoded_final}' ni dekodla!")
    send(conn, ">>> ")
    ans4 = recv(conn)
    if ans4.lower() != final_word:
        send(conn, f"[-] 4-bosqich xato! To'g'ri: '{final_word}'")
        return
    send(conn, "[+] 4-bosqich o'tdi!")

    send(conn, "")
    send(conn, "★" * 50)
    send(conn, "  [!!] TABRIKLAYMAN! BARCHA BOSQICHLARDAN O'TDINGIZ!")
    send(conn, "  [!!] Siz haqiqiy GRAND MASTER socket dasturchisinisz!")
    send(conn, "★" * 50)
    send(conn, f"[>] GRAND MASTER FLAG: {FLAGS[10]}")

# ─── Server ishga tushirish ──────────────────────────────────
CHALLENGES = {
    9001: challenge_1,
    9002: challenge_2,
    9003: challenge_3,
    9004: challenge_4,
    9005: challenge_5,
    9006: challenge_6,
    9007: challenge_7,
    9008: challenge_8,
    9009: challenge_9,
    9010: challenge_10,
}

def handle_client(conn, addr, challenge_func):
    """Har bir ulanishni alohida thread'da boshqaradi."""
    print(f"[+] Yangi ulanish: {addr}")
    try:
        challenge_func(conn, addr)
    except (ConnectionResetError, BrokenPipeError):
        print(f"[-] Ulanish uzildi: {addr}")
    except Exception as e:
        print(f"[-] Xato ({addr}): {e}")
    finally:
        conn.close()
        print(f"[*] Ulanish yopildi: {addr}")

def start_server(port, challenge_func):
    """Berilgan portda server ishga tushiradi."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(10)
    print(f"[*] Challenge {list(CHALLENGES.keys()).index(port)+1} serveri port {port} da ishlamoqda...")

    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr, challenge_func), daemon=True)
            t.start()
        except Exception as e:
            print(f"[-] Server xatosi (port {port}): {e}")

# ─── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Python CTF Socket Challenges Server")
    print("=" * 60)
    print()
    print("  PORTLAR VA CHALLENGELAR:")
    print("  Port 9001 -> Challenge 1: Salom de (HELLO yubor)")
    print("  Port 9002 -> Challenge 2: So'zni teskari yubor")
    print("  Port 9003 -> Challenge 3: 3 ta matematik savol")
    print("  Port 9004 -> Challenge 4: ROT13 dekodlash")
    print("  Port 9005 -> Challenge 5: Base64 dekodlash")
    print("  Port 9006 -> Challenge 6: Parol topish")
    print("  Port 9007 -> Challenge 7: Sezar shifri")
    print("  Port 9008 -> Challenge 8: 5 ta matematik savol")
    print("  Port 9009 -> Challenge 9: ASCII → Matn")
    print("  Port 9010 -> Challenge 10: Grand Final (4 bosqich)")
    print()
    print("  Server to'xtatish uchun: Ctrl+C")
    print("=" * 60)
    print()

    threads = []
    for port, func in CHALLENGES.items():
        t = threading.Thread(target=start_server, args=(port, func), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Server to'xtatildi.")
