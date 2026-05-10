# 🔴 Red Team Framework

<div align="center">

![Red Team Framework](https://img.shields.io/badge/Red%20Team-Framework-red?style=for-the-badge&logo=kalilinux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A full end-to-end offensive security framework built from scratch.**  
Automates the complete penetration testing kill chain — from recon to reporting.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Dashboard](#-web-dashboard) • [Phases](#-phases) • [Disclaimer](#-disclaimer)

</div>

---

## 📸 Screenshots

### 🖥️ Web Dashboard — Overview
![Dashboard Overview](https://raw.githubusercontent.com/sureddyjithendrareddy/RedTeamFramework/main/screenshots/dashboard_overview.png)

> Real-time mission overview with risk scoring, findings table, and live terminal output.

---

### 📡 C2 Console — Agent Management
![C2 Console](https://raw.githubusercontent.com/sureddyjithendrareddy/RedTeamFramework/main/screenshots/c2_console.png)

> Command & Control console with connected agents, interactive shell, and live command execution.

---

### 🔍 Recon Results
![Recon Results](https://raw.githubusercontent.com/sureddyjithendrareddy/RedTeamFramework/main/screenshots/recon_results.png)

> Automated subdomain enumeration, port scanning, and Shodan OSINT results.

---

### 💀 Exploitation — CVE Scanner
![Exploitation](https://raw.githubusercontent.com/sureddyjithendrareddy/RedTeamFramework/main/screenshots/exploitation.png)

> CVE vulnerability scanner with severity ratings, payload generator, and web attack testing.

---

### 📄 Auto-Generated PDF Report
![PDF Report](https://raw.githubusercontent.com/sureddyjithendrareddy/RedTeamFramework/main/screenshots/report.png)

> Professional penetration test report auto-generated with findings, risk scores, and remediation advice.

---

## 🎯 Features

| Phase | Capability |
|-------|-----------|
| 🔍 **Recon** | Subdomain enumeration, port scanning, Shodan OSINT, email harvesting, GitHub leak detection |
| 💀 **Exploitation** | CVE scanning via NVD API, payload generation, SQLi/XSS testing, directory bruteforcing |
| 🔓 **Post-Exploit** | PrivEsc checks, SUID detection, cron job analysis, persistence mechanisms, lateral movement |
| 📡 **C2** | Custom command & control server, Python agent with callback, interactive handler console |
| 🖥️ **Dashboard** | Full web UI with live terminal, agent management, risk scoring, findings table |
| 📄 **Reporting** | Auto-generated professional PDF pentest report with CVSS scores and remediation |

---

## 🛠️ Tech Stack

```
Language    →  Python 3
Web UI      →  Flask + HTML/CSS/JS
C2 Server   →  Flask REST API
Port Scanner→  python-nmap
OSINT       →  Shodan API
CVE Lookup  →  NVD National Vulnerability Database API
Reporting   →  fpdf2
Terminal UI →  Rich
```

---

## ⚙️ Installation

### Prerequisites
```bash
# Kali Linux recommended
sudo apt update && sudo apt install python3 python3-pip nmap git -y
```

### Clone & Setup
```bash
# Clone the repository
git clone https://github.com/sureddyjithendrareddy/RedTeamFramework.git
cd RedTeamFramework

# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Target
```bash
# Edit config file with your target details
nano config.py
```

```python
TARGET_DOMAIN = "target-domain.com"   # Target domain
TARGET_IP     = "XX.XX.XX.XX"         # Target IP address
SHODAN_KEY    = "YOUR_SHODAN_KEY"     # Get free key at shodan.io
KALI_IP       = "YOUR_KALI_IP"        # Your machine IP (hostname -I)
TARGET_URL    = "http://target.com"   # Full target URL
SUBNET        = "XX.XX.XX.0/24"       # Target subnet
TESTER_NAME   = "Your Name"           # Your name for report
COMPANY_NAME  = "Your Company"        # Company for report
```

---

## 🚀 Usage

### Option 1 — Run Full Assessment (CLI)
```bash
sudo ~/RedTeamFramework/myenv/bin/python3 main.py
```

This runs all 5 phases automatically and generates a PDF report.

---

### Option 2 — Web Dashboard (Recommended)

Open **4 terminals** and run each:

**Terminal 1 — C2 Server:**
```bash
cd RedTeamFramework
sudo myenv/bin/python3 c2/server.py
```

**Terminal 2 — C2 Agent:**
```bash
cd RedTeamFramework
myenv/bin/python3 c2/agent.py
```

**Terminal 3 — Dashboard:**
```bash
cd RedTeamFramework
myenv/bin/python3 dashboard/app.py
```

**Terminal 4 — Full Assessment (optional):**
```bash
cd RedTeamFramework
sudo myenv/bin/python3 main.py
```

Then open browser:
```
http://127.0.0.1:5000
```

---

## 🖥️ Web Dashboard

### Navigation

| Page | Description |
|------|-------------|
| **Overview** | Live stats, risk score, findings table, terminal |
| **Recon** | Subdomains, open ports, Shodan intel |
| **Exploitation** | CVE table, web findings |
| **Post-Exploit** | SUID binaries, cron jobs, lateral movement |
| **C2 Console** | Connected agents, interactive shell |
| **Payloads** | Reverse shell generator |
| **Report** | PDF report generator |
| **Settings** | Configure target & API keys |

### C2 Console Commands
```bash
whoami          # Get current user
id              # Get user ID and groups
sysinfo         # Full system information
pwd             # Current directory
ls -la          # List files
cat /etc/passwd # Read sensitive files
uname -a        # Kernel information
ps aux          # Running processes
ifconfig        # Network interfaces
```

---

## 📋 Phases

### Phase 1 — Reconnaissance
```
✓ Subdomain enumeration (crt.sh + brute force)
✓ Port scanning with service detection (nmap)
✓ Shodan OSINT lookup
✓ Email harvesting
✓ GitHub leak detection
```

### Phase 2 — Exploitation
```
✓ CVE scanning for each open service (NVD API)
✓ Reverse shell payload generation (bash, python, php, netcat, powershell)
✓ msfvenom payload commands
✓ Directory bruteforcing
✓ SQL injection testing
✓ XSS vulnerability testing
```

### Phase 3 — Post Exploitation
```
✓ System enumeration (OS, users, network, processes)
✓ Sudo permission check
✓ SUID binary detection with GTFOBins mapping
✓ Writable sensitive path detection
✓ Cron job enumeration
✓ Persistence mechanism analysis
✓ Lateral movement techniques
✓ Network host discovery
```

### Phase 4 — C2 (Command & Control)
```
✓ Custom Flask C2 server
✓ Python agent with automatic callback
✓ Encrypted agent registration
✓ Command queuing system
✓ Result collection and storage
✓ Interactive handler console
✓ Web dashboard integration
```

### Phase 5 — Reporting
```
✓ Professional PDF report generation
✓ Executive summary with risk overview
✓ Detailed findings with CVSS scores
✓ Severity-rated vulnerabilities
✓ Remediation recommendations
✓ Cover page with assessment details
```

---

## 📁 Project Structure

```
RedTeamFramework/
├── main.py                    # Main orchestrator
├── config.py                  # Target configuration
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── LICENSE                    # MIT License
│
├── recon/                     # Phase 1 - Reconnaissance
│   ├── subdomain_enum.py      # Subdomain enumeration
│   ├── port_scanner.py        # Port & service scanning
│   ├── osint.py               # Shodan & email OSINT
│   └── github_leak.py         # GitHub secret detection
│
├── exploitation/              # Phase 2 - Exploitation
│   ├── payload_generator.py   # Reverse shell payloads
│   ├── vuln_scanner.py        # CVE vulnerability scanner
│   └── web_attacks.py         # SQLi, XSS, dir busting
│
├── post_exploit/              # Phase 3 - Post Exploitation
│   ├── privesc.py             # Privilege escalation checks
│   ├── persistence.py         # Persistence mechanisms
│   └── lateral_movement.py    # Lateral movement
│
├── c2/                        # Phase 4 - Command & Control
│   ├── server.py              # C2 Flask server
│   ├── agent.py               # Target agent
│   └── handler.py             # Interactive console
│
├── dashboard/                 # Web Dashboard
│   ├── app.py                 # Dashboard Flask server
│   └── templates/
│       └── dashboard.html     # Full web UI
│
└── reporting/                 # Phase 5 - Reporting
    ├── report_generator.py    # PDF report generator
    └── templates.py           # Report styles & templates
```

---

## 🔑 API Keys Required

| Service | Purpose | Get it at |
|---------|---------|-----------|
| Shodan | IP intelligence & exposed services | [shodan.io](https://account.shodan.io/register) |
| Hunter.io (optional) | Email harvesting | [hunter.io](https://hunter.io) |
| GitHub (optional) | Leak detection | [github.com/settings/tokens](https://github.com/settings/tokens) |

---

## ⚠️ Disclaimer

```
This tool is for AUTHORIZED penetration testing and security research ONLY.

✓ Always obtain WRITTEN permission before testing any system
✓ Only test systems you own or have explicit authorization to test
✓ Follow responsible disclosure for any findings
✓ The author is NOT responsible for misuse or illegal activity
✓ Use on unauthorized systems is ILLEGAL and UNETHICAL

Tested on: Kali Linux 2024.x
```

---

## 📜 License

```
MIT License — Copyright (c) 2026 sureddyjithendrareddy
See LICENSE file for full details.
```

---

<div align="center">

Built with ❤️ for the cybersecurity community

⭐ Star this repo if you found it useful!

</div>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ATTACKER MACHINE (Kali)                  │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Phase 1  │───▶│ Phase 2  │───▶│ Phase 3  │              │
│  │  Recon   │    │ Exploit  │    │  Post-   │              │
│  └──────────┘    └──────────┘    │ Exploit  │              │
│       │                          └──────────┘              │
│       ▼                               │                    │
│  ┌──────────┐                         ▼                    │
│  │ Phase 5  │◀──────────────────┌──────────┐              │
│  │  Report  │                   │ Phase 4  │              │
│  └──────────┘                   │   C2     │              │
│       │                         └──────────┘              │
│       ▼                              ▲                     │
│  ┌─────────────────────────┐         │                    │
│  │    Web Dashboard :5000  │         │                    │
│  └─────────────────────────┘         │                    │
└─────────────────────────────────────│────────────────────┘
                                       │ agent callback
                              ┌────────┴───────┐
                              │ Target Machine  │
                              │ (Authorized)    │
                              └────────────────┘
```

### Component Flow

```
config.py
    │
    ├──▶ recon/           →  subdomain_enum.py, port_scanner.py, osint.py
    │                           ↓ recon_results.json
    ├──▶ exploitation/    →  vuln_scanner.py, payload_generator.py, web_attacks.py
    │                           ↓ exploitation_results.json
    ├──▶ post_exploit/    →  privesc.py, persistence.py, lateral_movement.py
    │                           ↓ post_exploit_results.json
    ├──▶ c2/              →  server.py (port 8080) ←→ agent.py (target)
    │                           ↓ agent callbacks
    ├──▶ reporting/       →  report_generator.py
    │                           ↓ pentest_report.pdf
    └──▶ dashboard/       →  app.py (port 5000)
                                ↕ reads all JSON results
                                ↕ triggers all phases via API
```

### Port Map

| Port | Service | Description |
|------|---------|-------------|
| `5000` | Dashboard | Web UI (Flask) |
| `8080` | C2 Server | Agent communication |
| `4444` | Listener | Reverse shell listener |

---

## 📁 File Structure

```
RedTeamFramework/
│
├── main.py                        # Orchestrates all 5 phases
├── config.py                      # Target IP, API keys, settings
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Excludes sensitive files
│
├── recon/                         # Phase 1 — Reconnaissance
│   ├── __init__.py
│   ├── subdomain_enum.py          # crt.sh + brute force enumeration
│   ├── port_scanner.py            # nmap port + service detection
│   ├── osint.py                   # Shodan API + email harvesting
│   └── github_leak.py             # GitHub secret detection
│
├── exploitation/                  # Phase 2 — Exploitation
│   ├── __init__.py
│   ├── payload_generator.py       # Bash, Python, PHP, PS reverse shells
│   ├── vuln_scanner.py            # CVE lookup via NVD API
│   ├── web_attacks.py             # SQLi, XSS, directory bruteforce
│   └── payloads/                  # Generated payloads (gitignored)
│
├── post_exploit/                  # Phase 3 — Post-Exploitation
│   ├── __init__.py
│   ├── privesc.py                 # SUID, sudo, cron checks
│   ├── persistence.py             # Cron + SSH key persistence
│   └── lateral_movement.py       # Network discovery + SSH access
│
├── c2/                            # Phase 4 — Command & Control
│   ├── __init__.py
│   ├── server.py                  # Flask C2 server (port 8080)
│   ├── agent.py                   # Python agent for target machine
│   └── handler.py                 # Interactive CLI console
│
├── reporting/                     # Phase 5 — Reporting
│   ├── __init__.py
│   ├── report_generator.py        # PDF pentest report builder
│   └── templates.py               # Styles, severity, remediation tips
│
├── dashboard/                     # Web Dashboard
│   ├── app.py                     # Flask dashboard server (port 5000)
│   └── templates/
│       └── dashboard.html         # Full web UI
│
└── utils/                         # Shared utilities
```

### Output Files (auto-generated, gitignored)

```
recon_results.json                 # Phase 1 output
exploitation_results.json          # Phase 2 output
post_exploit_results.json          # Phase 3 output
pentest_report.pdf                 # Final PDF report
```
