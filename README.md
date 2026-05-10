# 🔴 Red Team Framework

A full end-to-end offensive security framework built from scratch.
Covers every phase of a real penetration test engagement.

## 🎯 Features

| Phase | Capability |
|-------|-----------|
| Recon | Subdomain enum, port scanning, Shodan OSINT, email harvest, GitHub leak detection |
| Exploitation | CVE scanning, payload generation, web attack testing (SQLi, XSS, dir busting) |
| Post Exploit | PrivEsc checks, SUID detection, persistence, lateral movement |
| C2 | Custom command & control server, agent, interactive handler console |
| Reporting | Auto-generated professional PDF pentest report |

## 🛠️ Tech Stack
- Python 3
- Flask (C2 server)
- python-nmap (port scanning)
- Shodan API (OSINT)
- NVD API (CVE lookup)
- fpdf2 (report generation)
- Rich (terminal UI)

## ⚙️ Setup

```bash
git clone https://github.com/YOURUSERNAME/RedTeamFramework
cd RedTeamFramework
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## 🚀 Usage

```bash
# Configure your target in main.py
nano main.py

# Run full assessment
sudo python3 main.py

# Start C2 server (separate terminal)
python3 c2/server.py

# Start C2 handler (separate terminal)
python3 c2/handler.py
```

## ⚠️ Legal Disclaimer
This tool is for authorized penetration testing only.
Always obtain written permission before testing any system.
The author is not responsible for misuse.

## 📋 Requirements
See requirements.txt
