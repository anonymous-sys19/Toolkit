#!/usr/bin/python
import argparse
from Partials import URL_Lookup
from Partials import Whois
# Asegúrate de que DNS_Lookup.py se encuentra en la carpeta Partials
from Partials import DNS_Lookup
import subprocess
import platform
import random
from colorama import init, Fore, Style

import importlib.util
import pkg_resources
import sys

init(autoreset=True)


def check_requirements(requirements_file='requirements.txt'):
    with open(requirements_file, 'r') as file:
        requirements = file.readlines()

    missing_packages = []
    for requirement in requirements:
        package_name = requirement.split('==')[0]
        if not importlib.util.find_spec(package_name):
            missing_packages.append(requirement.strip())

    if missing_packages:
        print(Fore.RED + "The following packages are missing:")
        for package in missing_packages:
            print(Fore.RED + f"- {package}")
        install_missing_packages(missing_packages)
    else:
        print(Fore.GREEN + "All required packages are installed.")


def install_missing_packages(packages):
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', *packages])
        print(Fore.GREEN + "All missing packages were installed successfully.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to install packages: {e}")


def print_banner():
    banners = []
    try:
        with open('./Partials/Banner/banners.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            banners = content.split('\n\n\n')

        if banners:
            print(Fore.GREEN + Style.BRIGHT + random.choice(banners))
        else:
            print(Fore.RED + "No banners found.")
    except Exception as e:
        print(Fore.RED + f"Error reading banners: {e}")


def ip_lookup(ip):
    print(Fore.YELLOW + f"Performing IP Lookup for {ip}...")
    # Aquí deberías implementar la funcionalidad real de IP Lookup


def port_scanner(ip, port_range):
    print(Fore.YELLOW +
          f"Running Port Scanner on {ip} with range {port_range}...")
    # Aquí deberías implementar la funcionalidad real de Port Scanner


def dns_lookup(domain):
    print(Fore.YELLOW + f"Performing DNS Lookup for {domain}...")
    DNS_Lookup.dns_lookup(domain)


def url_lookup_func(url):
    print(Fore.YELLOW + f"Performing URL Lookup for {url}...")
    URL_Lookup.url_lookup(url)


def traceroute(host):
    print(Fore.YELLOW + f"Performing Traceroute to {host}...")
    try:
        system = platform.system().lower()
        if system == 'windows':
            result = subprocess.run(
                ["tracert", host], capture_output=True, text=True)
        else:
            result = subprocess.run(
                ["traceroute", host], capture_output=True, text=True)
        print(Fore.GREEN + result.stdout)
    except Exception as e:
        print(Fore.RED + f"An error occurred while performing traceroute: {e}")


def whois(domain):
    print(Fore.YELLOW + f"Performing WHOIS Lookup for {domain}...")
    Whois.Whois(domain)


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description=Fore.CYAN + "AnonimoSys19 Toolkit")
    parser.add_argument('--ip-lookup', action='store_true',
                        help=Fore.CYAN + 'Perform an IP Lookup for a given IP address')
    parser.add_argument('--port-scan', nargs=2, metavar=('IP', 'RANGE'),
                        help=Fore.CYAN + 'Perform a Port Scan on a given IP address and port range')
    parser.add_argument('--dns-lookup', action='store_true',
                        help=Fore.CYAN + 'Perform a DNS Lookup for a given domain')
    parser.add_argument('--url-lookup', action='store_true',
                        help=Fore.CYAN + 'Perform a URL Lookup for a given URL')
    parser.add_argument('--traceroute', action='store_true',
                        help=Fore.CYAN + 'Perform a Traceroute to a given host')
    parser.add_argument('--whois', action='store_true',
                        help=Fore.CYAN + 'Perform a WHOIS lookup for a given domain')
    parser.add_argument(
        '--target', type=str, help=Fore.CYAN + 'URL or IP address to perform the selected operation on')

    args = parser.parse_args()

    if args.ip_lookup and args.target:
        ip_lookup(args.target)
    elif args.port_scan:
        ip, port_range = args.port_scan
        port_scanner(ip, port_range)
    elif args.dns_lookup and args.target:
        dns_lookup(args.target)
    elif args.url_lookup and args.target:
        url_lookup_func(args.target)
    elif args.traceroute and args.target:
        traceroute(args.target)
    elif args.whois and args.target:
        whois(args.target)
    else:
        parser.print_help()
        print(Fore.RED + "No valid option provided or missing URL. Please use --help for more information.")


if __name__ == "__main__":
    try:
        check_requirements()
        main()
    except Exception as e:
        print(Fore.RED + f"An error occurred during execution: {e}")
    finally:
        print(Fore.CYAN + "Cleaning up resources...")
        # Add any necessary cleanup code here
