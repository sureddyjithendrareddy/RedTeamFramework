REPORT_STYLES = {
    'header_color': (20, 20, 20),
    'accent_color': (220, 50, 50),
    'success_color': (0, 180, 0),
    'warning_color': (255, 165, 0),
    'critical_color': (220, 50, 50),
    'high_color': (255, 100, 0),
    'medium_color': (255, 165, 0),
    'low_color': (0, 180, 0),
}

SEVERITY_RATINGS = {
    'CRITICAL': 'Immediate action required. System fully compromised.',
    'HIGH': 'Urgent remediation needed within 24-48 hours.',
    'MEDIUM': 'Remediation needed within 30 days.',
    'LOW': 'Remediation recommended within 90 days.',
    'INFO': 'Informational finding, no immediate action required.'
}

REMEDIATION_TIPS = {
    'sqli': 'Use parameterized queries and prepared statements. Never concatenate user input into SQL queries.',
    'xss': 'Sanitize and encode all user input. Implement Content Security Policy (CSP) headers.',
    'open_port': 'Close unnecessary ports. Implement firewall rules to restrict access.',
    'outdated_service': 'Update to latest stable version. Subscribe to security advisories.',
    'weak_ssh': 'Disable password authentication. Use SSH keys only. Restrict SSH access by IP.',
    'suid': 'Remove unnecessary SUID bits. Follow principle of least privilege.',
    'cron': 'Audit cron jobs regularly. Ensure scripts are not world-writable.',
    'default_creds': 'Change all default credentials immediately. Implement password policy.',
}
