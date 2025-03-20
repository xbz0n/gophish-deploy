# GoPhish-Deploy

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/Language-Python%203-blue" alt="Language">
  <img src="https://img.shields.io/badge/Platform-Linux-orange" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

<p align="center">
  <b>GoPhish-Deploy</b> is an automated deployment script for the GoPhish phishing framework, configuring it with SSL and secure defaults.
</p>

<p align="center">
  <a href="https://xbz0n.sh"><img src="https://img.shields.io/badge/Blog-xbz0n.sh-red" alt="Blog"></a>
</p>

---

## Overview

GoPhish-Deploy automates the deployment and configuration of the [GoPhish](https://github.com/gophish/gophish) phishing framework. The script installs all necessary dependencies, configures SSL certificates, and sets up the environment for a production-ready deployment.

## Features

- **Fully automated** - Complete installation and configuration in one script
- **SSL ready** - Automatic certificate generation with Certbot
- **Secure defaults** - Pre-configured with security best practices
- **Custom modifications** - Removes server headers and changes tracking parameters
- **Auto-start** - Configures GoPhish to start on system reboot
- **User-friendly** - Simple setup requiring only a domain name

## System Compatibility

| OS | Compatibility | Feature Support |
|----|---------------|-----------------|
| Ubuntu | ✅ | Full support |
| Debian | ✅ | Full support |
| Other Linux | ⚠️ | May require modifications |

## Requirements

- Linux-based operating system (tested on Ubuntu/Debian)
- Root privileges
- A valid domain name pointing to the server

## Installation

```bash
# Clone the repository
git clone https://github.com/xbz0n/gophish-deploy.git
cd gophish-deploy

# Run the deployment script with your domain
python GoPhish-Deploy.py your-domain.com
```

## Usage

### Basic Deployment

```bash
python GoPhish-Deploy.py example.com
```

### Accessing the Admin Panel

After deployment, access the GoPhish admin panel:

```bash
# Set up an SSH tunnel
ssh root@<your-server-ip> -L 3333:127.0.0.1:3333

# Then open in your browser
# https://127.0.0.1:3333
# Login with:
# Username: admin
# Password: gophish@123
```

## Script Workflow

1. Updates system and installs dependencies
2. Installs Go 1.12 runtime environment
3. Clones and builds the GoPhish project
4. Applies custom modifications to improve security
5. Generates SSL certificates using Certbot
6. Configures GoPhish to use HTTPS
7. Sets up auto-start on system reboot
8. Provides access instructions using SSH tunnel

## Detailed Functionality

| Function | Description |
|----------|-------------|
| System Update | Updates package lists and installs required dependencies |
| Go Installation | Installs Go 1.12 required to build GoPhish |
| Security Modifications | Removes X-Server header and changes tracking parameter from "rid" to "fname" |
| Database Configuration | Sets a default admin password and disables password change requirement |
| SSL Configuration | Generates and configures SSL certificates for secure connections |
| Auto-start | Creates a cron job to start GoPhish automatically on system reboot |

## Logs and Debugging

- Logs are stored in `/var/log/gophish`
- To manually start GoPhish:
  ```bash
  cd /opt/gophish
  ./gophish
  ```

## Troubleshooting

If you encounter issues:
- Ensure you are running the script with root privileges
- Verify your domain is correctly pointing to the server
- Check that port 80 and 443 are available for Certbot and GoPhish
- Examine the GoPhish logs for specific error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- **Ivan Spiridonov (xbz0n)** - [Blog](https://xbz0n.sh) | [GitHub](https://github.com/xbz0n)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The [GoPhish](https://github.com/gophish/gophish) project for their excellent phishing framework
- The security testing community for inspiration
