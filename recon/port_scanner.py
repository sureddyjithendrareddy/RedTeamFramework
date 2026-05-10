import nmap
from rich.console import Console
from rich.table import Table

console = Console()

def scan_ports(target, ports="1-1000"):
    """Scan ports and detect services"""
    console.print(f"[cyan][*] Scanning {target} on ports {ports}[/cyan]")
    
    nm = nmap.PortScanner()
    nm.scan(target, ports, arguments='-sV -T4')
    
    results = []
    table = Table(title=f"Port Scan Results - {target}")
    table.add_column("Port", style="cyan")
    table.add_column("State", style="green")
    table.add_column("Service", style="yellow")
    table.add_column("Version", style="white")

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                state = nm[host][proto][port]['state']
                service = nm[host][proto][port]['name']
                version = nm[host][proto][port]['version']
                
                results.append({
                    'port': port,
                    'state': state,
                    'service': service,
                    'version': version
                })
                table.add_row(str(port), state, service, version)

    console.print(table)
    return results
