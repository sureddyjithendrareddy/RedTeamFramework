import requests
from rich.console import Console

console = Console()

def shodan_lookup(ip, api_key):
    """Look up IP on Shodan"""
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        info = {
            'ip': ip,
            'org': data.get('org', 'N/A'),
            'os': data.get('os', 'N/A'),
            'ports': data.get('ports', []),
            'vulns': list(data.get('vulns', {}).keys()),
            'hostnames': data.get('hostnames', [])
        }
        
        console.print(f"[green][+] Shodan Info for {ip}:[/green]")
        for k, v in info.items():
            console.print(f"    {k}: {v}")
        
        return info
    except Exception as e:
        console.print(f"[red][-] Shodan lookup failed: {e}[/red]")
        return {}

def get_emails(domain):
    """Scrape emails from Hunter.io (free tier)"""
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key=YOUR_KEY"
        r = requests.get(url, timeout=10)
        data = r.json()
        emails = [e['value'] for e in data.get('data', {}).get('emails', [])]
        console.print(f"[green][+] Found {len(emails)} emails[/green]")
        return emails
    except Exception as e:
        console.print(f"[red][-] Email enum failed: {e}[/red]")
        return []
