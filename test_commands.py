#!/usr/bin/env python3
"""
SEA HORSE v3.0.0 - Command Tester
Tests all major SeaHorse commands
"""

import sys
import time
import json
import subprocess
import os
from typing import Dict, List, Tuple

# Color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Test cases - (command, expected_success, description)
TEST_COMMANDS = [
    # Basic commands
    ("help", True, "Display help menu"),
    ("status", True, "Show system status"),
    ("system", True, "Show system info"),
    ("time", True, "Show current time"),
    ("date", True, "Show current date"),
    ("datetime", True, "Show datetime"),
    
    # Network commands
    ("ping 127.0.0.1", True, "Ping localhost"),
    ("ping google.com", True, "Ping google.com"),
    ("traceroute 127.0.0.1", True, "Traceroute localhost"),
    
    # IP Management
    ("add_ip 192.168.1.100 Test IP", True, "Add IP to monitoring"),
    ("list_ips", True, "List managed IPs"),
    ("ip_info 192.168.1.100", True, "Get IP info"),
    ("remove_ip 192.168.1.100", True, "Remove IP from monitoring"),
    
    # CRUNCH commands
    ("crunch_charset", True, "List available charsets"),
    ("crunch_simple 4 6 lowercase", True, "Generate simple wordlist"),
    ("crunch 4 6 abc", True, "Generate wordlist with custom charset"),
    ("crunch_list", True, "List generated wordlists"),
    
    # Phishing commands
    ("phish_facebook", True, "Generate Facebook phishing link"),
    ("phish_instagram", True, "Generate Instagram phishing link"),
    ("phish_twitter", True, "Generate Twitter phishing link"),
    ("phishing_links", True, "List phishing links"),
    
    # Traffic commands
    ("traffic_types", True, "List traffic types"),
    ("traffic_status", True, "Check traffic status"),
    ("traffic_logs 5", True, "View traffic logs"),
    
    # SSH commands (if SSH server configured)
    # These are commented out as they require actual SSH servers
    # ("ssh_list", True, "List SSH servers"),
    
    # Threat commands
    ("threats", True, "View recent threats"),
]

def run_command(command: str) -> Tuple[bool, str, float]:
    """Execute a command and return result"""
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, 'seahorse.py', '--cmd', command],
            capture_output=True,
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        execution_time = time.time() - start_time
        return success, output, execution_time
    except subprocess.TimeoutExpired:
        return False, "Command timed out", 30.0
    except Exception as e:
        return False, str(e), time.time() - start_time

def test_commands_interactive():
    """Test commands in interactive mode using pexpect or similar"""
    # This is a simpler approach using subprocess
    results = []
    
    print(f"{Colors.CYAN}{Colors.BOLD}┌────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}│        SEA HORSE v3.0.0                    │{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}│        Command Tester                      │{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}└────────────────────────────────────────────┘{Colors.RESET}")
    print()
    
    print(f"{Colors.BLUE}📌 Running {len(TEST_COMMANDS)} tests...{Colors.RESET}")
    print()
    
    passed = 0
    failed = 0
    
    for i, (cmd, expected, desc) in enumerate(TEST_COMMANDS, 1):
        print(f"{Colors.YELLOW}Test {i}/{len(TEST_COMMANDS)}: {desc}{Colors.RESET}")
        print(f"  Command: {cmd}")
        
        success, output, exec_time = run_command(cmd)
        
        if success == expected:
            print(f"  {Colors.GREEN}✅ PASSED ({exec_time:.2f}s){Colors.RESET}")
            passed += 1
            # Show first line of output
            output_lines = output.strip().split('\n')
            if output_lines and output_lines[0]:
                print(f"    Output: {output_lines[0][:80]}")
        else:
            print(f"  {Colors.RED}❌ FAILED ({exec_time:.2f}s){Colors.RESET}")
            failed += 1
            if output:
                print(f"    Error: {output[:200]}")
        print()
    
    # Summary
    print(f"{Colors.BLUE}┌────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.BLUE}│        TEST SUMMARY                        │{Colors.RESET}")
    print(f"{Colors.BLUE}└────────────────────────────────────────────┘{Colors.RESET}")
    print()
    print(f"  {Colors.GREEN}✅ Passed: {passed}{Colors.RESET}")
    print(f"  {Colors.RED}❌ Failed: {failed}{Colors.RESET}")
    print(f"  {Colors.YELLOW}📊 Total: {len(TEST_COMMANDS)}{Colors.RESET}")
    print()
    
    if failed == 0:
        print(f"{Colors.GREEN}🎉 All tests passed! SeaHorse is working correctly.{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠️ Some tests failed. Check your configuration.{Colors.RESET}")
    
    return passed, failed

def test_imports():
    """Test all imports"""
    print(f"{Colors.BLUE}📌 Testing imports...{Colors.RESET}")
    
    imports = [
        'cryptography',
        'cryptography.fernet',
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
        'selenium'
    ]
    
    failed = []
    for imp in imports:
        try:
            __import__(imp)
            print(f"  {Colors.GREEN}✅ {imp}{Colors.RESET}")
        except ImportError:
            print(f"  {Colors.RED}❌ {imp}{Colors.RESET}")
            failed.append(imp)
    
    return failed

def main():
    """Main test runner"""
    print(f"{Colors.CYAN}🐴 SeaHorse Command Tester v3.0.0{Colors.RESET}")
    print()
    
    # Check if seahorse.py exists
    if not os.path.exists('seahorse.py'):
        print(f"{Colors.RED}❌ seahorse.py not found!{Colors.RESET}")
        print(f"Please run this script from the SeaHorse directory.")
        sys.exit(1)
    
    # Test imports
    import_failures = test_imports()
    print()
    
    if import_failures:
        print(f"{Colors.YELLOW}⚠️ Some imports failed. Install missing packages: pip install -r requirements.txt{Colors.RESET}")
        print()
    
    # Run command tests
    passed, failed = test_commands_interactive()
    
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()