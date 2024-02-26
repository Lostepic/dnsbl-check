import asyncio
import pydnsbl
from pydnsbl.providers import BASE_PROVIDERS, Provider
import logging
from netaddr import IPNetwork
from datetime import datetime
import os
import requests

# IP addresses to check
ip_list = ['192.0.2.0/24', '203.0.113.0/24']

# Discord Webhook settings
discord_webhook_url = "DISCORD-WEBHHOK"

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file
logging.basicConfig(filename=os.path.join('logs', f'blacklist_check_{datetime.now().strftime("%Y%m%d")}.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s')

def read_dnsbls_from_file(file_path='dnsbls.txt'):
    with open(file_path, 'r') as file:
        dnsbls = [line.strip() for line in file.readlines() if line.strip()]
    return dnsbls

def create_custom_providers(dnsbl_domains):
    return [Provider(domain) for domain in dnsbl_domains]

def notify_discord(blacklisted_ips):
    content = '\n'.join([f"IP {ip} is blacklisted on: {', '.join(detected_by)}" for ip, detected_by in blacklisted_ips])
    data = {"content": f"Blacklisted IP Alert:\n{content}"}
    response = requests.post(discord_webhook_url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

async def check_single_ip(ip_checker, single_ip, blacklisted_ips):
    result = await ip_checker.check_async(str(single_ip))
    if result.blacklisted:
        message = f"IP {single_ip} is blacklisted on: {', '.join(result.detected_by)}"
        print(message)
        logging.info(message)
        blacklisted_ips.append((str(single_ip), result.detected_by))
    else:
        message = f"IP {single_ip} is not blacklisted."
        print(message)
        logging.info(message)

async def check_ip_blacklist(ip_list, custom_providers):
    providers = BASE_PROVIDERS + custom_providers
    ip_checker = pydnsbl.DNSBLIpChecker(providers=providers)
    blacklisted_ips = []

    tasks = []
    for ip in ip_list:
        for single_ip in IPNetwork(ip):
            tasks.append(check_single_ip(ip_checker, single_ip, blacklisted_ips))
    await asyncio.gather(*tasks)

    # If we found any blacklisted IPs, notify via Discord
    if blacklisted_ips:
        notify_discord(blacklisted_ips)

# Read the list of DNSBL domains from file and create custom providers
dnsbl_domains = read_dnsbls_from_file()
custom_providers = create_custom_providers(dnsbl_domains)

# Run the asynchronous function
asyncio.run(check_ip_blacklist(ip_list, custom_providers))
