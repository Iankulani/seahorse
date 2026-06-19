#!/bin/bash
# SeaHorse v3.0.0 - Linux/macOS Installation Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${CYAN}${BOLD}┌────────────────────────────────────────────┐${RESET}"
echo -e "${CYAN}${BOLD}│        SEA HORSE v3.0.0                    │${RESET}"
echo -e "${CYAN}${BOLD}│        Installation Script                 │${RESET}"
echo -e "${CYAN}${BOLD}└────────────────────────────────────────────┘${RESET}"
echo

# Check Python version
echo -e "${BLUE}📌 Checking Python version...${RESET}"
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$PYTHON_VERSION" | awk -F. '{print $1}') -lt 3 ]] || [[ $(echo "$PYTHON_VERSION" | awk -F. '{print $2}') -lt 7 ]]; then
    echo -e "${RED}❌ Python 3.7+ required. Found: $PYTHON_VERSION${RESET}"
    exit 1
fi
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${RESET}"
echo

# Check OS
OS=$(uname -s)
echo -e "${BLUE}🖥️ Detected OS: ${OS}${RESET}"

# Install system dependencies
echo -e "${BLUE}📦 Installing system dependencies...${RESET}"

if [[ "$OS" == "Linux" ]]; then
    echo -e "${YELLOW}Detected Linux. Installing dependencies...${RESET}"
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-dev build-essential \
            nmap nikto curl dnsutils traceroute openssh-client \
            chromium-browser chromium-chromedriver || true
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip python3-devel gcc \
            nmap nikto curl bind-utils traceroute openssh-clients \
            chromium chromium-headless chromedriver || true
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip python3-devel gcc \
            nmap nikto curl bind-utils traceroute openssh-clients \
            chromium chromium-headless chromedriver || true
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --needed python-pip python \
            nmap nikto curl dnsutils traceroute openssh \
            chromium chromedriver || true
    else
        echo -e "${YELLOW}⚠️ Could not detect package manager. Please install manually:${RESET}"
        echo "  python3-pip, nmap, nikto, curl, dnsutils, traceroute, openssh-client, chromium, chromedriver"
    fi
    
elif [[ "$OS" == "Darwin" ]]; then
    echo -e "${YELLOW}Detected macOS. Installing dependencies...${RESET}"
    
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}⚠️ Homebrew not found. Installing...${RESET}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install python3 nmap nikto curl dnsutils traceroute openssh || true
    brew install --cask chromium || true
    
else
    echo -e "${YELLOW}⚠️ Unsupported OS. Please install dependencies manually.${RESET}"
fi

echo

# Install Python packages
echo -e "${BLUE}🐍 Installing Python packages...${RESET}"

# Ensure pip is up to date
python3 -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}📄 Installing from requirements.txt...${RESET}"
    python3 -m pip install -r requirements.txt
else
    echo -e "${YELLOW}⚠️ requirements.txt not found. Installing core packages...${RESET}"
    python3 -m pip install cryptography colorama requests psutil paramiko \
        scapy python-whois qrcode pyshorteners Flask discord.py telethon \
        slack-sdk selenium webdriver-manager dnspython pyOpenSSL
fi

echo

# Verify installation
echo -e "${BLUE}🔍 Verifying installation...${RESET}"
python3 requirements_check.py

# Create directories
echo -e "${BLUE}📁 Creating SeaHorse directories...${RESET}"
mkdir -p .seahorse/{payloads,workspaces,scans,reports,phishing_pages,wordlists,ssh_keys,web_ui}
mkdir -p .seahorse/{traffic_logs,captured_credentials,phishing_templates,custom_phishing,webhooks}
mkdir -p .seahorse/{nikto_results,time_history,ssh_logs,whatsapp_session,signal_session}

echo
echo -e "${CYAN}${BOLD}┌────────────────────────────────────────────┐${RESET}"
echo -e "${CYAN}${BOLD}│        INSTALLATION COMPLETE!              │${RESET}"
echo -e "${CYAN}${BOLD}│        🐴 SEA HORSE v3.0.0                 │${RESET}"
echo -e "${CYAN}${BOLD}└────────────────────────────────────────────┘${RESET}"
echo
echo -e "${GREEN}✅ SeaHorse has been installed successfully!${RESET}"
echo
echo -e "${CYAN}📌 To run SeaHorse:${RESET}"
echo -e "  ${BOLD}python3 seahorse.py${RESET}"
echo
echo -e "${CYAN}📌 For web interface:${RESET}"
echo -e "  Open http://localhost:8080 in your browser"
echo
echo -e "${CYAN}📌 For help:${RESET}"
echo -e "  Type 'help' in the SeaHorse terminal"
echo
echo -e "${CYAN}📌 Check dependencies:${RESET}"
echo -e "  ${BOLD}python3 requirements_check.py${RESET}"
echo

# Make script executable
chmod +x seahorse.py requirements_check.py 2>/dev/null || true

echo -e "${GREEN}🐴 Happy hacking with SeaHorse!${RESET}"