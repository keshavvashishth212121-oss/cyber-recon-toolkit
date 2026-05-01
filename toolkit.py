import os
import socket
import requests
import threading
import time
import json
from datetime import datetime

open_ports = []
lock = threading.Lock()

# 🔹 Common Services
services = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL"
}

# 🔹 Banner
def banner():
    print("""
    #################################################
    #                                               #
    #         CYBER RECON TOOLKIT v3.0              #
    #        Created by: Keshav Vashishth           #
    #                                               #
    #################################################
    """)

# 🔹 IP Lookup
def ip_lookup():
    ip = input("Enter IP Address: ")
    print(f"\nFetching details for {ip}...\n")
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data['status'] == 'success':
            print(f"[+] Country : {data['country']}")
            print(f"[+] Region  : {data['regionName']}")
            print(f"[+] City    : {data['city']}")
            print(f"[+] ISP     : {data['isp']}")
            print(f"[+] Lat/Lon : {data['lat']}, {data['lon']}")
        else:
            print("[-] Invalid IP or not found.")
    except Exception as e:
        print(f"[-] Error: {e}")

# 🔹 Scan Single Port
def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        
        if result == 0:
            service = services.get(port, "Unknown")
            with lock:
                print(f"[OPEN] Port {port} ({service})")
                open_ports.append({"port": port, "service": service})
        
        s.close()
    except:
        pass

# 🔹 Port Scanner
def port_scanner():
    global open_ports
    open_ports = []

    target = input("Enter Target IP: ")

    # ✅ IP validation
    try:
        socket.inet_aton(target)
    except:
        print("[-] Invalid IP Address!")
        return

    try:
        start_port = int(input("Start Port: "))
        end_port = int(input("End Port: "))
    except:
        print("[-] Invalid port range!")
        return

    print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

    start_time = time.time()
    threads = []
    MAX_THREADS = 100

    for port in range(start_port, end_port + 1):
        while threading.active_count() > MAX_THREADS:
            pass
        
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    # 🔹 Report
    print("\n========== SCAN REPORT ==========")
    print(f"Target: {target}")
    print(f"Open Ports: {open_ports if open_ports else 'None'}")
    print(f"Time Taken: {round(end_time - start_time, 2)} sec")

    # 🔹 Save Report
    save = input("\nSave report? (y/n): ")
    if save.lower() == 'y':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # TXT
        txt_file = f"scan_{timestamp}.txt"
        with open(txt_file, "w") as f:
            f.write(f"Target: {target}\n")
            f.write(f"Open Ports: {open_ports}\n")
            f.write(f"Time: {round(end_time - start_time, 2)} sec\n")

        # JSON
        json_file = f"scan_{timestamp}.json"
        data = {
            "target": target,
            "open_ports": open_ports,
            "time": round(end_time - start_time, 2)
        }
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        print(f"[+] Reports saved: {txt_file}, {json_file}")

# 🔹 Main Menu
def main_menu():
    while True:
        banner()
        print("1. Port Scanner (Fast)")
        print("2. IP Geolocation")
        print("3. Exit")
        
        choice = input("\nChoose an option: ")

        if choice == '1':
            port_scanner()
            input("\nPress Enter to continue...")
        elif choice == '2':
            ip_lookup()
            input("\nPress Enter to continue...")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

        os.system('cls' if os.name == 'nt' else 'clear')

# 🔹 Run
if __name__ == "__main__":
    main_menu()