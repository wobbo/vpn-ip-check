# vpn-ip-check

Simple Linux script to verify whether your VPN connection is active by checking your public IP address.

Originally created to quickly confirm VPN status. Later extended with optional speedtest support.

## Features

* Shows current public IP address
* Helps confirm whether VPN is active
* Detects IP changes
* Optional speedtest support
* Lightweight and cron-friendly
* Works on Raspberry Pi, Linux servers and other Debian-based systems

<img width="482" height="466" alt="image" src="https://github.com/user-attachments/assets/c52108a3-b800-4d34-ac2a-7c9111f724ea" />

## Example use cases

* Check if VPN is connected
* Detect unexpected VPN disconnects
* Monitor IP changes automatically
* Quick remote connection diagnostics

## Requirements

Required:

* bash
* curl

Install speedtest-cli:

```bash
wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz
tar -xzf ookla-speedtest-1.2.0-linux-aarch64.tgz
chmod +x speedtest
sudo mv speedtest /usr/local/bin/
speedtest --accept-license --accept-gdpr
```

## Usage

Run:

```bash
bash vpn-ip-check.sh
```

Example cron job (run every 10 minutes):

```bash
/full/path/to/vpn-ip-check.sh
```

## Example output

```
Public IP: 185.xxx.xxx.xxx
VPN status: ACTIVE
Speedtest: optional
```

## Supported systems

Tested on:

* Raspberry Pi OS
* Debian
* Ubuntu

Should work on most Linux distributions with bash and curl installed.

## License

MIT License
