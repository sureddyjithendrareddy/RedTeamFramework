import dns.resolver
import requests
from rich.console import Console

console = Console()

def enumerate_subdomains(domain):
    """Enumerate subdomains using wordlist + crt.sh"""
    found = []

    # Method 1: crt.sh certificate transparency
    console.print(f"[cyan][*] Fetching subdomains from crt.sh for {domain}[/cyan]")
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=10)
        data = r.json()
        for entry in data:
            name = entry['name_value'].strip()
            for sub in name.split('\n'):
                if sub not in found:
                    found.append(sub)
    except Exception as e:
        console.print(f"[red][-] crt.sh failed: {e}[/red]")

    # Method 2: DNS brute force with common wordlist
    wordlist = ['www', 'mail', 'ftp', 'admin', 'vpn', 'dev',
                'staging', 'api', 'test', 'portal', 'secure']
    console.print(f"[cyan][*] Brute forcing common subdomains...[/cyan]")
    for word in wordlist:
        subdomain = f"{word}.{domain}"
        try:
            dns.resolver.resolve(subdomain, 'A')
            if subdomain not in found:
                found.append(subdomain)
                console.print(f"[green][+] Found: {subdomain}[/green]")
        except:
            pass

    return found
