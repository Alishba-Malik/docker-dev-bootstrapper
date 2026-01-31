## Docker Dev Bootstrapper
My **go-to** development container setup. I use it whenever I need a clean, reproducible environment with all the essential development tools pre-installed. It’s designed to just work across Linux and Windows, automating Docker installation if necessary and giving me a ready-to-use dev workspace inside a container.

## Repository Structure

```
├── docker-compose.yml# Defines the interactive dev container
├── Dockerfile# Base Ubuntu 22.04 image with essential tools
└── docker_setup.py# Cross-platform Docker installation and validation
```
### Kick Start

### **Clone the repo:**

```bash
git clone https://github.com/Alishba-Malik/docker-dev-bootstrapper.git
cd docker-dev-bootstrapper
```

### Run the setup script

**For Linux:** 

Run it as root user

```bash
sudo python3 docker_setup.py
```

> After installation, log out & back in if you were added to the Docker group… you know the drill 😉
> 

**For Windows (Administrator):**

Remember: run it as an administrator

```powershell
python docker_setup.py

```

> Installs Docker Desktop via winget. You might need a reboot… and WSL2 enabled… wink wink
> 

### 3) Jump into the container

```bash
docker compose run dev
```

You’ll land in `/workspace` with all your project files ready to go… ready, set, code ;)

## Useful Commands

```
# Start a fresh container
docker compose run dev

# Rebuild image (Dockerfile changed)
docker compose build

# Stop all containers
docker compose down
```

**My dev sandbox for life. I use it for pretty much everything**  ;)

