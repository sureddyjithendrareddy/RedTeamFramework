from fpdf import FPDF
from datetime import datetime
import json
import os
from reporting.templates import REPORT_STYLES, SEVERITY_RATINGS, REMEDIATION_TIPS
from rich.console import Console

console = Console()

class PentestReport(FPDF):
    def __init__(self, target, tester, company):
        super().__init__()
        self.target = target
        self.tester = tester
        self.company = company
        self.styles = REPORT_STYLES

    def header(self):
        # Red header bar
        self.set_fill_color(*self.styles['accent_color'])
        self.rect(0, 0, 210, 15, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, '  RED TEAM FRAMEWORK - PENETRATION TEST REPORT', ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_fill_color(*self.styles['accent_color'])
        self.rect(0, 285, 210, 15, 'F')
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'  CONFIDENTIAL | {self.target} | Page {self.page_no()}', align='L')

    def cover_page(self):
        self.add_page()

        # Big red banner
        self.set_fill_color(*self.styles['accent_color'])
        self.rect(0, 40, 210, 60, 'F')

        self.set_y(55)
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'PENETRATION TEST REPORT', ln=True, align='C')
        self.set_font('Helvetica', '', 14)
        self.cell(0, 10, 'Red Team Security Assessment', ln=True, align='C')

        # Details box
        self.set_y(120)
        self.set_fill_color(240, 240, 240)
        self.rect(20, 120, 170, 80, 'F')

        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.set_x(30)
        self.ln(5)

        details = [
            ('Target', self.target),
            ('Assessed By', self.tester),
            ('Organization', self.company),
            ('Date', datetime.now().strftime('%B %d, %Y')),
            ('Classification', 'CONFIDENTIAL'),
        ]

        for label, value in details:
            self.set_x(30)
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(*self.styles['accent_color'])
            self.cell(50, 12, label + ':', ln=False)
            self.set_font('Helvetica', '', 11)
            self.set_text_color(0, 0, 0)
            self.cell(0, 12, value, ln=True)

    def section_title(self, title):
        self.ln(5)
        self.set_fill_color(*self.styles['accent_color'])
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, f'  {title}', ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def severity_badge(self, severity):
        colors = {
            'CRITICAL': self.styles['critical_color'],
            'HIGH': self.styles['high_color'],
            'MEDIUM': self.styles['warning_color'],
            'LOW': self.styles['success_color'],
            'INFO': (100, 100, 200)
        }
        color = colors.get(severity.upper(), (128, 128, 128))
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 9)
        self.cell(25, 7, severity.upper(), fill=True, align='C')
        self.set_text_color(0, 0, 0)

    def executive_summary(self, recon_data, exploit_data, post_data):
        self.add_page()
        self.section_title('1. EXECUTIVE SUMMARY')

        # Count findings
        total_ports = len(recon_data.get('recon', {}).get('ports', []))
        total_subdomains = len(recon_data.get('recon', {}).get('subdomains', []))
        total_vulns = sum(len(v) for v in exploit_data.get('vulnerabilities', {}).values())
        total_dirs = len(exploit_data.get('dirs', []))
        suid_count = len(post_data.get('privesc', {}).get('suid_exploitable', []))

        summary = f"""This penetration test was conducted against {self.target} to identify security vulnerabilities
and assess the overall security posture. The assessment covered reconnaissance, exploitation,
post-exploitation, and lateral movement phases using a custom Red Team Framework.

KEY FINDINGS SUMMARY:
- Open Ports Discovered: {total_ports}
- Subdomains Enumerated: {total_subdomains}
- CVE Vulnerabilities Found: {total_vulns}
- Exposed Directories: {total_dirs}
- Exploitable SUID Binaries: {suid_count}
"""
        self.set_font('Helvetica', '', 11)
        self.multi_cell(0, 7, summary)

        # Risk meter
        self.ln(5)
        self.section_title('2. RISK OVERVIEW')

        risk_items = [
            ('Critical', total_vulns, self.styles['critical_color']),
            ('High', suid_count, self.styles['high_color']),
            ('Medium', total_dirs, self.styles['warning_color']),
            ('Low', total_ports, self.styles['success_color']),
        ]

        for label, count, color in risk_items:
            self.set_font('Helvetica', 'B', 11)
            self.cell(40, 10, label + ':')
            self.set_fill_color(*color)
            bar_width = min(count * 10, 120)
            if bar_width > 0:
                self.cell(bar_width, 8, '', fill=True)
            self.set_font('Helvetica', '', 10)
            self.cell(20, 10, f'  {count} findings')
            self.ln()

    def recon_section(self, recon_data):
        self.add_page()
        self.section_title('3. RECONNAISSANCE FINDINGS')

        recon = recon_data.get('recon', {})

        # Subdomains
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, '3.1 Subdomains Discovered', ln=True)
        subdomains = recon.get('subdomains', [])
        self.set_font('Helvetica', '', 10)
        if subdomains:
            for sub in subdomains[:20]:
                self.set_x(20)
                self.cell(5, 7, '-')
                self.cell(0, 7, str(sub), ln=True)
        else:
            self.cell(0, 7, 'No subdomains found.', ln=True)

        # Open Ports
        self.ln(5)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, '3.2 Open Ports & Services', ln=True)

        ports = recon.get('ports', [])
        if ports:
            # Table header
            self.set_fill_color(*self.styles['accent_color'])
            self.set_text_color(255, 255, 255)
            self.set_font('Helvetica', 'B', 10)
            self.cell(25, 8, 'Port', fill=True, border=1)
            self.cell(25, 8, 'State', fill=True, border=1)
            self.cell(40, 8, 'Service', fill=True, border=1)
            self.cell(0, 8, 'Version', fill=True, border=1, ln=True)
            self.set_text_color(0, 0, 0)

            self.set_font('Helvetica', '', 10)
            for i, port in enumerate(ports):
                fill = i % 2 == 0
                self.set_fill_color(245, 245, 245)
                self.cell(25, 7, str(port.get('port', '')), fill=fill, border=1)
                self.cell(25, 7, str(port.get('state', '')), fill=fill, border=1)
                self.cell(40, 7, str(port.get('service', '')), fill=fill, border=1)
                self.cell(0, 7, str(port.get('version', ''))[:40], fill=fill, border=1, ln=True)
        else:
            self.set_font('Helvetica', '', 10)
            self.cell(0, 7, 'No open ports found.', ln=True)

    def exploitation_section(self, exploit_data):
        self.add_page()
        self.section_title('4. VULNERABILITY FINDINGS')

        vulns = exploit_data.get('vulnerabilities', {})
        dirs = exploit_data.get('dirs', [])

        if vulns:
            for service, cve_list in vulns.items():
                self.set_font('Helvetica', 'B', 11)
                self.cell(0, 9, f'Service: {service}', ln=True)

                for cve in cve_list:
                    self.set_x(15)
                    severity = str(cve.get('severity', 'MEDIUM'))
                    self.severity_badge(severity)
                    self.set_font('Helvetica', 'B', 10)
                    self.cell(0, 7, f"  {cve.get('cve_id', 'N/A')} - Score: {cve.get('score', 'N/A')}", ln=True)
                    self.set_x(15)
                    self.set_font('Helvetica', '', 9)
                    desc = str(cve.get('description', ''))[:120]
                    self.multi_cell(0, 6, f"  {desc}")
                    self.ln(2)
        else:
            self.set_font('Helvetica', '', 10)
            self.cell(0, 7, 'No CVE vulnerabilities found.', ln=True)

        # Exposed directories
        if dirs:
            self.ln(5)
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 10, '4.2 Exposed Directories', ln=True)
            self.set_font('Helvetica', '', 10)
            for d in dirs:
                status = d.get('status', '')
                url = d.get('url', '')
                color = self.styles['success_color'] if status == 200 else self.styles['warning_color']
                self.set_text_color(*color)
                self.cell(20, 7, f'[{status}]')
                self.set_text_color(0, 0, 0)
                self.cell(0, 7, url, ln=True)

    def post_exploit_section(self, post_data):
        self.add_page()
        self.section_title('5. POST-EXPLOITATION FINDINGS')

        # SUID binaries
        suid = post_data.get('privesc', {}).get('suid_exploitable', [])
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, '5.1 Exploitable SUID Binaries', ln=True)

        if suid:
            for item in suid:
                self.set_x(15)
                self.severity_badge('HIGH')
                self.set_font('Helvetica', '', 10)
                self.cell(0, 7, f"  {item.get('binary', '')} -> {item.get('exploit', '')}", ln=True)
        else:
            self.set_font('Helvetica', '', 10)
            self.cell(0, 7, 'No exploitable SUID binaries found.', ln=True)

        # Persistence
        self.ln(5)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, '5.2 Persistence Mechanisms', ln=True)
        persistence = post_data.get('persistence', [])
        self.set_font('Helvetica', '', 10)
        if persistence:
            for item in persistence:
                self.set_x(15)
                self.cell(0, 7, f"- {item.get('name', '')} at {item.get('path', '')}", ln=True)
        else:
            self.cell(0, 7, 'No suspicious persistence found.', ln=True)

    def recommendations_section(self):
        self.add_page()
        self.section_title('6. RECOMMENDATIONS')

        recs = [
            ('CRITICAL', 'Patch all services with known CVEs immediately',
             'Update all services to latest versions. Subscribe to CVE alerts for installed software.'),
            ('HIGH', 'Remove unnecessary SUID binaries',
             REMEDIATION_TIPS['suid']),
            ('HIGH', 'Harden SSH configuration',
             REMEDIATION_TIPS['weak_ssh']),
            ('MEDIUM', 'Restrict exposed web directories',
             'Disable directory listing. Remove sensitive files from web root.'),
            ('MEDIUM', 'Implement Web Application Firewall',
             REMEDIATION_TIPS['xss'] + ' ' + REMEDIATION_TIPS['sqli']),
            ('LOW', 'Regular security audits',
             'Conduct quarterly penetration tests and monthly vulnerability scans.'),
        ]

        for i, (severity, title, detail) in enumerate(recs):
            self.set_font('Helvetica', 'B', 11)
            self.cell(10, 9, f'{i+1}.')
            self.severity_badge(severity)
            self.set_font('Helvetica', 'B', 11)
            self.cell(0, 9, f'  {title}', ln=True)
            self.set_x(20)
            self.set_font('Helvetica', '', 10)
            self.multi_cell(0, 6, detail)
            self.ln(3)


def generate_full_report(target, tester, company,
                          recon_data, exploit_data, post_data,
                          output_file="pentest_report.pdf"):
    console.print(f"[cyan][*] Generating penetration test report...[/cyan]")

    report = PentestReport(target=target, tester=tester, company=company)

    # Build all sections
    report.cover_page()
    report.executive_summary(recon_data, exploit_data, post_data)
    report.recon_section(recon_data)
    report.exploitation_section(exploit_data)
    report.post_exploit_section(post_data)
    report.recommendations_section()

    # Save PDF
    report.output(output_file)
    console.print(f"[bold green][+] Report saved to {output_file}[/bold green]")
    return output_file
