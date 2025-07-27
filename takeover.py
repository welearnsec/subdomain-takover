# enhanced_takeover.py #subdomaintakeover

import requests
import dns.resolver
import sys
import concurrent.futures

# List of known takeover services
FINGERPRINTS = [
    {
        "service": "GitHub Pages",
        "cname": "github.io",
        "fingerprint": "There isn't a GitHub Pages site here."
    },
    {
        "service": "Heroku",
        "cname": "herokudns.com",
        "fingerprint": "No such app"
    },
    {
        "service": "AWS/S3",
        "cname": "s3.amazonaws.com",
        "fingerprint": "NoSuchBucket"
    },
    {
        "service": "Surge.sh",
        "cname": "surge.sh",
        "fingerprint": "project not found"
    },
    {
        "service": "Bitbucket",
        "cname": "bitbucket.io",
        "fingerprint": "Repository not found"
    },
    {
        "service": "Pantheon",
        "cname": "pantheonsite.io",
        "fingerprint": "404 error unknown site"
    },
    {
        "service": "Cloudfront",
        "cname": "cloudfront.net",
        "fingerprint": "The request could not be satisfied"
    },
]

# Resolve CNAME record
def get_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        return str(answers[0].target).rstrip('.')
    except:
        return None

# Match CNAME to a known service
def detect_service_from_cname(cname):
    for fp in FINGERPRINTS:
        if fp["cname"] in cname:
            return fp["service"]
    return None

# Match HTTP fingerprint
def detect_service_from_http(content):
    for fp in FINGERPRINTS:
        if fp["fingerprint"].lower() in content.lower():
            return fp["service"]
    return None

# Main check
def check_subdomain(subdomain):
    cname = get_cname(subdomain)
    cname_service = detect_service_from_cname(cname) if cname else None

    try:
        r = requests.get(f"http://{subdomain}", timeout=5)
        body_service = detect_service_from_http(r.text)
    except:
        body_service = None

    if cname_service or body_service:
        service = body_service or cname_service
        return f"[!] {subdomain} -> Possible takeover via {service} (CNAME: {cname})"
    else:
        return f"[+] {subdomain} -> No obvious takeover detected"

# Main handler
def main(file_path):
    with open(file_path, "r") as f:
        subdomains = [line.strip() for line in f if line.strip()]
    
    print(f"[i] Checking {len(subdomains)} subdomains...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_subdomain, subdomains)

    for result in results:
        print(result)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python enhanced_takeover.py subdomains.txt")
        sys.exit(1)
    main(sys.argv[1])
