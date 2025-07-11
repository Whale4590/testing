#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

def extract_version(link):
    # match the version naming convention 'V#R#'
    match = re.search(r'RHEL_9_(V\d+R\d+)', link)
    return match.group(1) if match else None

def version_key(v):
    # Sort versions and return the latest
    match = re.match(r'V(\d+)R(\d+)', v)
    return tuple(map(int, match.groups())) if match else (0, 0)

def find_latest_rhel9_stig():
    url = "https://public.cyber.mil/stigs/downloads/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    stig_links = soup.find_all('a', href=True)
    rhel9_links = [a for a in stig_links if 'RHEL_9' in a['href'] and a['href'].endswith('.zip')]
    version_map = {}
    for a in rhel9_links:
        version = extract_version(a['href'])
        if version:
            version_map[version] = a['href']
    
    if not version_map:
        return None

    latest_version = max(version_map.keys(), key=version_key)
    return version_map[latest_version]

if __name__ == "__main__":
    latest_stig = find_latest_rhel9_stig()
    if latest_stig:
        print(latest_stig)
    



