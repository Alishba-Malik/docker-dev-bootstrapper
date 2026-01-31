import os
import platform
import subprocess
import sys
import shutil

# ---------------- Helper functions ----------------
def run(cmd, ignore_errors=False):
    print(f"[+] Running: {cmd}")
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        if ignore_errors:
            print(f"[!] Warning: Command failed but skipping...")
        else:
            print(f"[-] Command failed: {cmd}")
            sys.exit(1)

def command_exists(cmd):
    return shutil.which(cmd) is not None

def is_root():
    if platform.system().lower() == "windows":
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0

def docker_compose_available():
    try:
        subprocess.check_output("docker compose version", shell=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# ---------------- Linux installation ----------------
def install_docker_linux(distro):
    if not is_root():
        print("[-] Please run this script with sudo on Linux.")
        sys.exit(1)

    if distro == "kali":
        print("[+] Kali Linux detected - Cleaning up potential conflicts")
        
        # We use ignore_errors=True because it's okay if these aren't there yet
        run("apt-get purge -y docker-buildx docker-compose-v2 docker-compose", ignore_errors=True)
        run("apt-get autoremove -y", ignore_errors=True)
        
        # Remove old Docker repo if exists
        run("rm -f /etc/apt/sources.list.d/docker.list")

        # Install prerequisites
        run("apt-get update")
        run("apt-get install -y ca-certificates curl gnupg lsb-release")

        # Set up keyrings
        run("install -m 0755 -d /etc/apt/keyrings")
        run("curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc")
        run("chmod a+r /etc/apt/keyrings/docker.asc")

        # Add Docker repo using Debian codename (bookworm)
        run("""tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: bookworm
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF""")

        run("apt-get update")

        # Install Docker CE + Compose v2
        run("apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")

    else:
        print("[+] Installing Docker using official Docker script...")
        run("apt-get update")
        run("apt-get install -y ca-certificates curl gnupg lsb-release")
        run("curl -fsSL https://get.docker.com | sh")
        run("apt-get install -y docker-compose-plugin")

    # Enable and start Docker
    run("systemctl enable docker")
    run("systemctl start docker")

    # Add current user to docker group
    user = os.environ.get("SUDO_USER") or os.environ.get("USER")
    if user:
        print(f"[+] Adding {user} to docker group...")
        run(f"usermod -aG docker {user}")
        print("[!] Log out and log back in for docker group changes to take effect.")

# ---------------- Windows installation ----------------
def install_docker_windows():
    print("[+] Windows detected")

    if not is_root():
        print("[-] Please run this script as Administrator on Windows.")
        return

    if not command_exists("winget"):
        print("[-] winget not found.")
        print("[-] Please install Docker Desktop manually from:")
        print("    https://docs.docker.com/desktop/install/windows-install/")
        return

    print("[+] Installing Docker Desktop via winget...")
    run("winget install -e --id Docker.DockerDesktop")

    print("[!] Docker Desktop installed.")
    print("[!] Please reboot and ensure WSL2 is enabled.")
    print("[!] After reboot, open Docker Desktop once before using docker.")

# ---------------- Main script ----------------
def main():
    system = platform.system().lower()
    print(f"[+] Detected OS: {system}")

    if system == "linux":
        try:
            distro = platform.freedesktop_os_release().get("ID", "").lower()
        except AttributeError:
            # Fallback for older Python versions
            distro = "unknown"
            
        if distro in ["ubuntu", "debian", "kali"]:
            if not command_exists("docker"):
                install_docker_linux(distro)
            else:
                print("[+] Docker already installed")
        else:
            print(f"[-] Unsupported Linux distro: {distro}")
            sys.exit(1)

    elif system == "windows":
        if not command_exists("docker"):
            install_docker_windows()
        else:
            print("[+] Docker already installed")

    else:
        print("[-] Unsupported OS")
        sys.exit(1)

    # Docker Compose check
    if docker_compose_available():
        print("[+] Docker Compose (v2) available")
    else:
        print("[-] Docker Compose not found")

    print("\n[✓] Setup complete")
    print("Next step:")
    print("  docker compose run dev")

if __name__ == "__main__":
    main()
