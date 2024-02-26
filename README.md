# DNSBL IP Checker

This project is a Python script that checks a list of IPv4 addresses to see if they are blacklisted on any DNS-based Blackhole List (DNSBL) providers. The script logs the results of the checks and sends a discord notification if any of the IPs are blacklisted.
(This is a fork of https://github.com/Accuris-Technologies-Ltd/dnsbl-check with some adjustments for my own use)

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- asyncio
- pydnsbl
- netaddr
- logging

You can install these packages using pip:

```bash
pip install asyncio pydnsbl netaddr
```

## Configuration

Before running the script, replace the placeholders in the .py and IP list with your actual data:

```python
# Discord Webhook settings
discord_webhook_url = "DISCORD-WEBHHOK"

# IP list
ip_list = ['192.0.2.0/24', '203.0.113.0/24']
```

- `discord_webhook_url` - Paste your discord webhook
- `ip_list` - The list of IP addresses or ranges you want to check. The IPs should be provided as strings in standard IPv4 format or CIDR notation.

In addition to the webhook change I have added a list of providers called dnsbls.txt which will be used alongside the default providers of pydnsbl you can add and remove providers as you want:

```bash
# dnsbls.txt
all.s5h.net
b.barracudacentral.org
bl.spamcop.net
blacklist.woody.ch
```

## Notice about DNS settings

Please ensure your system's DNS settings do not use Cloudflare or Quad9 DNS resolvers as these services are commonly blocked by the DNS-based Blackhole List (DNSBL) providers which are used by this script. You can check your DNS settings in the network settings of your operating system.

## Usage

To run the script, simply execute it with Python:

```bash
python check_blacklist.py
```

The script logs the results of the checks into a file in the 'logs' directory. The log files are named in the format 'blacklist_check_YYYYMMDD.log'. If any blacklisted IPs are found, a discord notification is sent to the webhook specified.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
