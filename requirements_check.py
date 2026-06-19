#!/usr/bin/env python3
"""
SEA HORSE v3.0.0 - Requirements Checker
Checks if all dependencies are installed properly
"""

import sys
import subprocess
import importlib.util
import pkg_resources
import os
import platform

REQUIRED_PACKAGES = [
    'cryptography',
    'colorama',
    'requests',
    'psutil',
    'paramiko',
    'scapy',
    'whois',
    'qrcode',
    'pyshorteners',
    'Flask',
    'discord',
    'telethon',
    'slack_sdk',
    'selenium',
    'webdriver_manager',
    'dnspython',
    'pyOpenSSL'
]

OPTIONAL_PACKAGES = [
    'selenium',
    'webdriver_manager',
    'discord',
    'telethon',
    'slack_sdk'
]

# Colors for output (fallback if colorama not installed)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        pkg_resources.get_distribution(package_name)
        return True, pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return False, None
    except Exception as e:
        return False, str(e)

def check_external_tool(tool_name):
    """Check if an external system tool is available"""
    import shutil
    return shutil.which(tool_name) is not None

def install_package(package_name, upgrade=False):
    """Attempt to install a package using pip"""
    try:
        cmd = [sys.executable, '-m', 'pip', 'install']
        if upgrade:
            cmd.append('--upgrade')
        cmd.append(package_name)
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Failed to install {package_name}: {e}{Colors.RESET}")
        return False

def check_python_version():
    """Check Python version requirements"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        return True, f"{version.major}.{version.minor}.{version.micro}"
    return False, f"{version.major}.{version.minor}.{version.micro}"

def check_system_info():
    """Display system information"""
    info = {
        'System': platform.system(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Architecture': platform.machine(),
        'Processor': platform.processor(),
        'Python Version': sys.version
    }
    return info

def check_selenium_requirements():
    """Check if Selenium and ChromeDriver are properly set up"""
    result = {"available": False, "message": ""}
    
    # Check if selenium is installed
    selenium_installed, _ = check_package('selenium')
    if not selenium_installed:
        return {"available": False, "message": "Selenium not installed"}
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        # Check for ChromeDriver manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            # Check if Chrome is available
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=options)
            driver.quit()
            return {"available": True, "message": "ChromeDriver configured correctly"}
        except ImportError:
            return {"available": False, "message": "webdriver-manager not installed"}
        except Exception as e:
            return {"available": False, "message": f"ChromeDriver setup error: {str(e)}"}
    except ImportError:
        return {"available": False, "message": "Selenium import failed"}

def main():
    print(f"{Colors.CYAN}{Colors.BOLD}┌────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}│        SEA HORSE v3.0.0                    │{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}│        Requirements Checker                │{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}└────────────────────────────────────────────┘{Colors.RESET}")
    print()
    
    # Python Version Check
    print(f"{Colors.BLUE}📌 Python Version Check{Colors.RESET}")
    py_ok, py_version = check_python_version()
    if py_ok:
        print(f"  {Colors.GREEN}✅ Python {py_version} (OK){Colors.RESET}")
    else:
        print(f"  {Colors.RED}❌ Python {py_version} (3.7+ required){Colors.RESET}")
    print()
    
    # System Information
    print(f"{Colors.BLUE}🖥️ System Information{Colors.RESET}")
    sys_info = check_system_info()
    print(f"  System: {sys_info['System']} {sys_info['Release']}")
    print(f"  Architecture: {sys_info['Architecture']}")
    print()
    
    # Package Checks
    print(f"{Colors.BLUE}📦 Package Dependencies{Colors.RESET}")
    print("  " + "─" * 50)
    
    failed_packages = []
    optional_failed = []
    
    for package in REQUIRED_PACKAGES:
        installed, version = check_package(package)
        is_optional = package in OPTIONAL_PACKAGES
        
        status = f"{Colors.GREEN}✅" if installed else f"{Colors.YELLOW}⚠️" if is_optional else f"{Colors.RED}❌"
        version_str = f"v{version}" if version else "Not installed"
        optional_marker = " (optional)" if is_optional else ""
        
        print(f"  {status} {package:<20} {version_str:<15} {optional_marker}{Colors.RESET}")
        
        if not installed:
            if is_optional:
                optional_failed.append(package)
            else:
                failed_packages.append(package)
    
    print()
    
    # External Tools Check
    print(f"{Colors.BLUE}🔧 External System Tools{Colors.RESET}")
    tools = ['ping', 'nmap', 'curl', 'dig', 'traceroute', 'ssh']
    
    for tool in tools:
        installed = check_external_tool(tool)
        status = f"{Colors.GREEN}✅" if installed else f"{Colors.YELLOW}⚠️"
        print(f"  {status} {tool:<15} {'Found' if installed else 'Not found (optional)'}{Colors.RESET}")
    
    print()
    
    # Selenium/ChromeDriver Check
    print(f"{Colors.BLUE}🌐 Selenium & ChromeDriver{Colors.RESET}")
    selenium_check = check_selenium_requirements()
    if selenium_check["available"]:
        print(f"  {Colors.GREEN}✅ {selenium_check['message']}{Colors.RESET}")
    else:
        print(f"  {Colors.YELLOW}⚠️ {selenium_check['message']} (WhatsApp feature will be disabled){Colors.RESET}")
    print()
    
    # Summary
    print(f"{Colors.BLUE}📊 Summary{Colors.RESET}")
    print("  " + "─" * 50)
    
    if failed_packages:
        print(f"{Colors.RED}❌ Missing required packages:{Colors.RESET}")
        for pkg in failed_packages:
            print(f"    - {pkg}")
        print(f"\n{Colors.YELLOW}💡 Install missing packages: pip install -r requirements.txt{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 Or: pip install {' '.join(failed_packages)}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}✅ All required packages are installed!{Colors.RESET}")
    
    if optional_failed:
        print(f"{Colors.YELLOW}⚠️ Optional packages missing:{Colors.RESET}")
        for pkg in optional_failed:
            print(f"    - {pkg} (feature disabled)")
    
    print()
    print(f"{Colors.CYAN}📌 To install all dependencies:{Colors.RESET}")
    print(f"  pip install -r requirements.txt")
    print()
    print(f"{Colors.CYAN}📌 To run SeaHorse:{Colors.RESET}")
    print(f"  python3 seahorse.py")
    print()
    
    if not failed_packages:
        print(f"{Colors.GREEN}✅ System ready for SeaHorse! 🐴{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}❌ Please install missing dependencies before running.{Colors.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())