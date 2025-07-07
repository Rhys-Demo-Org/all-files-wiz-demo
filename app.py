# vulnerable_app.py
# A simple Flask application with intentional vulnerabilities for security scanning demonstration.

from flask import Flask, request, render_template_string
import pickle
import subprocess
import yaml # PyYAML version 5.3.1 has a known vulnerability

# Outdated and vulnerable libraries
# PyYAML version 5.3.1 is vulnerable to arbitrary code execution.
# A newer version like 6.0 or the use of yaml.safe_load() is recommended.
#
# Requests version 2.22.0 has known security vulnerabilities.
# It is advisable to update to a more recent version.
import requests

app = Flask(__name__)

password = "test"

# --- Vulnerability 1: Insecure Deserialization ---
@app.route('/unpickle', methods=['POST'])
def unpickle_data():
    """
    This endpoint demonstrates insecure deserialization using pickle.
    Loading data directly from a request without sanitization can lead to
    remote code execution if the pickled data is crafted maliciously.
    Wiz Code and similar tools would flag the use of `pickle.loads` on external input.
    """
    pickled_data = request.get_data()
    try:
        # Vulnerable line: Deserializing untrusted data
        deserialized_data = pickle.loads(pickled_data)
        return f"Deserialized data: {deserialized_data}"
    except Exception as e:
        return f"An error occurred during deserialization: {e}"

# --- Vulnerability 2: Command Injection ---
@app.route('/lookup')
def dns_lookup():
    """
    This endpoint is vulnerable to command injection.
    It takes a 'domain' parameter from the URL and uses it directly in a shell command.
    An attacker could inject additional commands using shell separators like ';' or '&&'.
    Security scanners will identify the use of `subprocess.run` with `shell=True` and user input.
    """
    domain = request.args.get('domain')
    if domain:
        # Vulnerable line: User input is passed directly to a shell command
        command_output = subprocess.run(f"nslookup {domain}", shell=True, capture_output=True, text=True)
        return f"<pre>{command_output.stdout}{command_output.stderr}</pre>"
    return "Please provide a 'domain' parameter in the URL (e.g., /lookup?domain=example.com)"

# --- Vulnerability 3: Use of Outdated and Vulnerable Libraries ---
@app.route('/load_yaml')
def load_yaml_data():
    """
    This function uses an old and vulnerable version of PyYAML.
    PyYAML 5.3.1 is susceptible to arbitrary code execution when loading untrusted YAML.
    Code scanners will flag the use of this library version.
    """
    yaml_string = """
    !!python/object/new:os._wrap_close
    args: [!python/object/new:subprocess.Popen {args: ['touch', '/tmp/pwned']}]
    """
    try:
        # Vulnerable line: Using a known vulnerable library version.
        data = yaml.load(yaml_string, Loader=yaml.FullLoader)
        return f"Loaded YAML data (check /tmp/pwned): {data}"
    except Exception as e:
        return f"An error occurred while loading YAML: {e}"

@app.route('/')
def index():
    """
    The main page of the application with links to the vulnerable endpoints.
    """
    return render_template_string('''
        <h1>Vulnerable Python App</h1>
        <p>This application contains intentional vulnerabilities for security scanning tools to find.</p>
        <ul>
            <li><a href="/lookup?domain=google.com">Test Command Injection (nslookup google.com)</a></li>
            <li>
                <form action="/unpickle" method="post">
                    <p>Test Insecure Deserialization (This will execute `os.system("echo HELLO")` if pickled correctly):</p>
                    <input type="submit" value="Send Malicious Pickle">
                </form>
            </li>
             <li><a href="/load_yaml">Test Vulnerable PyYAML</a></li>
        </ul>
    ''')

if __name__ == '__main__':
    # To run this application:
    # 1. Make sure you have Flask installed: pip install Flask
    # 2. Install the vulnerable version of PyYAML: pip install PyYAML==5.3.1
    # 3. Install a vulnerable version of requests: pip install requests==2.22.0
    # 4. Run the script: python vulnerable_app.py
    app.run(debug=True)