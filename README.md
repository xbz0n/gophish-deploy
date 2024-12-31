# GoPhish Deployment Script

This repository provides a Python script to automate the deployment and configuration of the [GoPhish](https://github.com/gophish/gophish) phishing framework. The script installs all necessary dependencies, configures SSL certificates, and sets up the environment for a production-ready deployment.

## Features

- Automatic system updates and dependency installation.
- Installation of Go 1.12.
- Cloning and building the GoPhish project.
- Automatic SSL certificate generation using Certbot.
- Configuration of GoPhish to use SSL.
- Setting up GoPhish to start automatically on reboot.
- Custom database initialization and configuration.
- External IP fetching for easier access.

## Prerequisites

- A Linux-based operating system (tested on Ubuntu/Debian).
- Root privileges.
- A valid domain name pointing to the server.

## Usage

### Step 1: Clone the Repository

Clone this repository or download the script file:

```bash
git clone https://github.com/yourusername/gophish-deployment-script.git
cd gophish-deployment-script
```

### Step 2: Run the Script

Run the script with the required domain name:

```bash
python deploy_gophish.py <your-domain>
```

#### Example:

```bash
python deploy_gophish.py example.com
```

### Script Actions

1. **System Update and Dependency Installation:** Installs required packages like `unzip`, `sqlite3`, `certbot`, etc.
2. **Go Installation:** Installs Go 1.12, which is required to build GoPhish.
3. **Clone GoPhish Repository:** Clones the official GoPhish GitHub repository into `/opt/gophish`.
4. **Build GoPhish:** Compiles GoPhish and makes it executable.
5. **Configure SSL Certificates:** Uses Certbot to generate SSL certificates for the provided domain.
6. **Modify Configuration:** Updates the GoPhish configuration file to enable HTTPS and use the generated certificates.
7. **Set up Auto-Start:** Configures GoPhish to start automatically upon system reboot.
8. **Start GoPhish:** Starts the GoPhish service.

### Step 3: Access the GoPhish Admin Panel

After successful deployment, access the GoPhish admin panel:

1. Set up an SSH tunnel:
   ```bash
   ssh root@<your-server-ip> -L 3333:127.0.0.1:3333
   ```

2. Open your browser and visit:
   ```
   https://127.0.0.1:3333
   ```

3. Use the following credentials to log in:
   - **Username:** `admin`
   - **Password:** `gophish@123`

> **Note:** Change the default credentials after logging in for the first time.

## Logs and Debugging

- Logs are stored in `/var/log/gophish`.
- To manually start GoPhish:
  ```bash
  cd /opt/gophish
  ./gophish
  ```

## Troubleshooting

If the script encounters errors:
- Ensure you are running it with root privileges.
- Verify your domain is correctly pointing to the server.
- Check the log files for detailed error information.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
