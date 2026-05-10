import requests
from rich.console import Console

console = Console()

def search_github_leaks(domain, token=None):
    """Search GitHub for exposed secrets related to domain"""
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    
    queries = [
        f'"{domain}" password',
        f'"{domain}" api_key',
        f'"{domain}" secret',
        f'"{domain}" credentials'
    ]
    
    results = []
    for q in queries:
        try:
            url = f"https://api.github.com/search/code?q={requests.utils.quote(q)}"
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            items = data.get('items', [])
            for item in items[:3]:  # limit to 3 per query
                results.append({
                    'query': q,
                    'repo': item['repository']['full_name'],
                    'file': item['name'],
                    'url': item['html_url']
                })
                console.print(f"[yellow][!] Potential leak: {item['html_url']}[/yellow]")
        except Exception as e:
            console.print(f"[red][-] GitHub search failed: {e}[/red]")
    
    return results
