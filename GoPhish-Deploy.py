#!/usr/bin/env python3
'''
 ██████╗  ██████╗ ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗      ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
██╔════╝ ██╔═══██╗██╔══██╗██║  ██║██║██╔════╝██║  ██║      ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
██║  ███╗██║   ██║██████╔╝███████║██║███████╗███████║█████╗██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
██║   ██║██║   ██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║╚════╝██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
╚██████╔╝╚██████╔╝██║     ██║  ██║██║███████║██║  ██║      ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
 ╚═════╝  ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝      ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
                                                                                                                                                                                          
Created by: Ivan Spiridonov (xbz0n)
Website: https://xbz0n.sh
'''

import os
import subprocess
import sys
from pathlib import Path
import time
import requests

def run_command(command, check=True):
    """Run a system command and handle errors."""
    try:
        subprocess.run(command, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main(domain):
    if not domain:
        print("Usage: python deploy_gophish.py <domain>")
        sys.exit(1)

    print("Updating system and installing dependencies...")
    run_command("export DEBIAN_FRONTEND=noninteractive && apt update")
    run_command("apt -y install unzip sqlite3 net-tools certbot git wget gcc build-essential jq")

    print("Installing Go 1.12...")
    go_version = "go1.12.linux-amd64.tar.gz"

    run_command(f"wget https://go.dev/dl/{go_version}")
    run_command("rm -rf /usr/local/go")
    run_command(f"tar -C /usr/local -xzf {go_version}")
    run_command(f"rm -f {go_version}")
    os.environ["PATH"] += ":/usr/local/go/bin"

    go_version_check = subprocess.getoutput("go version")
    if "go version" in go_version_check:
        print(f"Go version installed successfully: {go_version_check}")
    else:
        print("Error: Go was not installed correctly.")
        sys.exit(1)

    print("Cloning GoPhish repository...")
    if not Path("/opt/gophish").exists():
        run_command("git clone https://github.com/gophish/gophish /opt/gophish")

    print("Applying custom modifications to GoPhish...")
    run_command("sed -i '/X-Server/d' /opt/gophish/controllers/phish.go")
    run_command("sed -i 's/\"rid\"/\"fname\"/g' /opt/gophish/controllers/phish.go")

    print("Building GoPhish...")
    run_command("cd /opt/gophish && go build .")
    run_command("chmod 755 /opt/gophish/gophish")

    print("Setting up log directory...")
    run_command("mkdir -p /var/log/gophish")

    print("Initializing GoPhish database...")
    run_command("cd /opt/gophish && ./gophish > /dev/null 2>&1 &")
    print("Waiting for GoPhish to initialize...")
    time.sleep(15)

    run_command("pkill -f gophish", check=False)

    print("Configuring GoPhish database...")
    run_command("sqlite3 /opt/gophish/gophish.db 'UPDATE users SET hash=\"$2a$10$pAbhayqOUEn8iSHvgkcmNe3VmpAWxjGDAuTGNrv4uIHRY3upXMB7.\" WHERE username=\"admin\";'")
    run_command("sqlite3 /opt/gophish/gophish.db 'UPDATE users SET password_change_required=\"0\" WHERE username=\"admin\";'")

    print("Setting up SSL certificates with Certbot...")
    run_command(f"certbot certonly --standalone --non-interactive --agree-tos -m admin@{domain} -d {domain}")

    print("Configuring GoPhish to use SSL...")
    gophish_config = "/opt/gophish/config.json"

    if Path(gophish_config).exists():
        domain_path = f"/etc/letsencrypt/live/{domain}"
        run_command(f"""
            jq '
            .admin_server.listen_url = "127.0.0.1:3333" |
            .admin_server.use_tls = true |
            .admin_server.cert_path = "{domain_path}/fullchain.pem" |
            .admin_server.key_path = "{domain_path}/privkey.pem" |
            .phish_server.listen_url = "0.0.0.0:443" |
            .phish_server.use_tls = true |
            .phish_server.cert_path = "{domain_path}/fullchain.pem" |
            .phish_server.key_path = "{domain_path}/privkey.pem"
            ' {gophish_config} > {gophish_config}.tmp && mv {gophish_config}.tmp {gophish_config}
        """)
        print("SSL configuration updated successfully.")
    else:
        print("Error: GoPhish configuration file not found!")
        sys.exit(1)

    print("Configuring GoPhish to start on reboot...")
    cron_entry = "@reboot root cd /opt/gophish && ./gophish > /dev/null 2>&1 &"
    with open("/etc/cron.d/gophish", "w") as cron_file:
        cron_file.write(cron_entry + "\n")

    print("Starting GoPhish...")
    run_command("cd /opt/gophish && ./gophish > /dev/null 2>&1 &")

    def get_external_ip():
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            return response.json()["ip"]
        except requests.RequestException as e:
            print(f"Error fetching external IP: {e}")
            sys.exit(1)

    external_ip = get_external_ip()

    print("Deployment complete!")
    print(f"Access the GoPhish admin panel with: ssh root@{external_ip} -L 3333:127.0.0.1:3333")
    print("Default username: admin")
    print("Default password: gophish@123")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python deploy_gophish.py <domain>")
        sys.exit(1)
    main(sys.argv[1])
