from flask import Flask, render_template, jsonify, request, send_file
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/results/recon')
def recon_results():
    data = load_json('recon_results.json')
    return jsonify(data) if data else ('', 404)


@app.route('/results/exploit')
def exploit_results():
    data = load_json('exploitation_results.json')
    return jsonify(data) if data else ('', 404)


@app.route('/results/post')
def post_results():
    data = load_json('post_exploit_results.json')
    return jsonify(data) if data else ('', 404)


@app.route('/run/recon', methods=['POST'])
def run_recon():
    try:
        from main import run_recon as do_recon
        import config
        do_recon(target_domain=config.TARGET_DOMAIN, target_ip=config.TARGET_IP, shodan_key=config.SHODAN_KEY)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/run/exploit', methods=['POST'])
def run_exploit():
    try:
        from main import run_exploitation
        import config
        recon_data = load_json('recon_results.json')
        run_exploitation(port_results=recon_data.get('recon', {}).get('ports', []), lhost=config.KALI_IP, target_url=config.TARGET_URL)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/run/postexploit', methods=['POST'])
def run_post():
    try:
        from main import run_post_exploitation
        import config
        run_post_exploitation(lhost=config.KALI_IP, lport=4444, subnet=config.SUBNET)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/run/report', methods=['POST'])
def run_report():
    try:
        from main import run_reporting
        data = request.json or {}
        run_reporting(
            recon_data=load_json('recon_results.json'),
            exploit_data=load_json('exploitation_results.json'),
            post_data=load_json('post_exploit_results.json'),
            target=data.get('target', 'Unknown'),
            tester=data.get('tester', 'Unknown'),
            company=data.get('company', 'Unknown')
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/download/report')
def download_report():
    path = os.path.join(BASE_DIR, 'pentest_report.pdf')
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'Report not generated yet'}), 404


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════╗
║   RED TEAM FRAMEWORK - DASHBOARD    ║
╠══════════════════════════════════════╣
║  Open: http://127.0.0.1:5000        ║
╚══════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
