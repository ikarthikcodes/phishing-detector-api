import re
import math
import csv
from urllib.parse import urlparse


# LOAD TRANCO DATA
TOP_DOMAINS = set()

try:
    with open("tranco.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                TOP_DOMAINS.add(row[1].strip().lower())
except:
    TOP_DOMAINS = set()


# HELPER
def get_core_domain(domain):
    parts = domain.split('.')
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain


# ENTROPY
def shannon_entropy(string):
    if not string:
        return 0
    prob = [float(string.count(c)) / len(string) for c in set(string)]
    return -sum([p * math.log2(p) for p in prob])


# CHECK IP
def has_ip(domain):
    return int(bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)))


# MAIN FUNCTION
def extract_features(url):
    try:
        if not isinstance(url, str):
            return [0]*23

        if not url.startswith("http"):
            url = "http://" + url

        url = url.strip().lower()
        parsed = urlparse(url)

    except:
        return [0]*23

    domain = parsed.netloc
    path = parsed.path

    if domain.startswith("www."):
        domain = domain[4:]

    # BASIC
    url_length = len(url)
    domain_length = len(domain)

    num_hyphens = url.count('-')
    num_at = url.count('@')
    num_qmark = url.count('?')
    num_and = url.count('&')
    num_equals = url.count('=')

    # CHARACTER STATS
    digits = sum(c.isdigit() for c in url)
    letters = sum(c.isalpha() for c in url)
    specials = len(re.findall(r'[^a-zA-Z0-9]', url))

    digit_ratio = digits / url_length if url_length else 0
    letter_ratio = letters / url_length if url_length else 0
    
    # DOMAIN STRUCTURE
    parts = domain.split('.')
    subdomains = len(parts) - 2 if len(parts) > 2 else 0

    too_many_subdomains = int(subdomains > 3)

    suspicious_subdomain = int(
        subdomains > 2 and any(word in domain for word in ["login", "secure", "account", "verify"])
    )

    # HTTPS
    is_https = int(parsed.scheme == 'https')

    # SUSPICIOUS WORDS
    suspicious_words = [
        'login', 'verify', 'signin', 'update',
        'password', 'bank', 'secure', 'account'
    ]
    has_suspicious_word = int(any(word in url for word in suspicious_words))

    # TLD
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf']
    has_suspicious_tld = int(any(domain.endswith(tld) for tld in suspicious_tlds))

    # STRUCTURAL FLAGS
    long_domain = int(domain_length > 30)
    many_hyphens = int(num_hyphens > 3)

    # IP + ENTROPY
    is_ip = has_ip(domain)
    entropy = shannon_entropy(url)

    #  REPUTATION FEATURE
    core_domain = get_core_domain(domain)
    is_top_domain = int(core_domain in TOP_DOMAINS) * 0.2

    # FINAL VECTOR (26 FEATURES)
    return [
        url_length,
        domain_length,
        num_hyphens,
        num_at,
        num_qmark,
        num_and,
        num_equals,
        digits,
        letters,
        specials,
        digit_ratio,
        letter_ratio,
        subdomains,
        too_many_subdomains,
        suspicious_subdomain,
        is_https,
        has_suspicious_word,
        has_suspicious_tld,
        long_domain,
        many_hyphens,
        is_ip,
        entropy,
        is_top_domain
    ]
import re
import math
import csv
from urllib.parse import urlparse

# LOAD TRANCO DATA
TOP_DOMAINS = set()

try:
    # Ensure this file exists in directory
    with open("tranco.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                # Store the full registered domain (e.g., google.com)
                TOP_DOMAINS.add(row[1].strip().lower())
except Exception as e:
    print(f"Warning: Could not load tranco.csv: {e}")
    TOP_DOMAINS = set()


# HELPERS
def get_core_domain(domain):
    """Extracts the registered domain (domain.tld)"""
    parts = domain.split('.')
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain

def shannon_entropy(string):
    """Calculates the randomness of a string (Phishing URLs are often high entropy)"""
    if not string:
        return 0
    prob = [float(string.count(c)) / len(string) for c in set(string)]
    return -sum([p * math.log2(p) for p in prob])

def has_ip(domain):
    """Checks if the domain is a raw IP address"""
    return int(bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)))


# MAIN EXTRACTION FUNCTION
def extract_features(url):
    try:
        if not isinstance(url, str) or not url.strip():
            return [0] * 23

        # Standardize URL for parsing
        original_url = url.strip()
        if not url.startswith("http"):
            url = "http://" + url

        url = url.lower()
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        
        # Remove WWW for domain analysis
        clean_domain = domain[4:] if domain.startswith("www.") else domain

    except Exception:
        return [0] * 23

    # BASIC COUNTS
    url_length = len(url)
    domain_length = len(clean_domain)
    num_hyphens = url.count('-')
    num_at = url.count('@')
    num_qmark = url.count('?')
    num_and = url.count('&')
    num_equals = url.count('=')

    #  CHARACTER RATIOS
    digits = sum(c.isdigit() for c in url)
    letters = sum(c.isalpha() for c in url)
    specials = len(re.findall(r'[^a-zA-Z0-9]', url))

    digit_ratio = digits / url_length if url_length else 0
    letter_ratio = letters / url_length if url_length else 0
    # DOMAIN STRUCTURE
    domain_parts = clean_domain.split('.')
    # Subdomains are parts beyond the 'domain.tld'
    subdomains = len(domain_parts) - 2 if len(domain_parts) > 2 else 0
    too_many_subdomains = int(subdomains > 3)

    # Keywords specifically in the domain/subdomain (High signal for phishing)
    suspicious_words = ['login', 'verify', 'signin', 'update', 'password', 'bank', 'secure', 'account']
    suspicious_subdomain = int(any(word in clean_domain for word in suspicious_words))

    #  SECURITY & TLD
    is_https = int(parsed.scheme == 'https')
    has_suspicious_word_overall = int(any(word in url for word in suspicious_words))
    
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf', '.top', '.xyz', '.bid']
    has_suspicious_tld = int(any(clean_domain.endswith(tld) for tld in suspicious_tlds))

    #  STRUCTURAL FLAGS
    long_domain = int(domain_length > 25)
    many_hyphens = int(num_hyphens > 3)

    #  TECHNICAL STATS
    is_ip = has_ip(clean_domain)
    entropy = shannon_entropy(url)

    #  REPUTATION (The "Is it Famous?" check)
    # FIX: Use 1.0 instead of 0.2 so the model actually notices it.
    core_domain = get_core_domain(clean_domain)
    is_top_domain = int(core_domain in TOP_DOMAINS)

    return [
        url_length,            
        domain_length,         
        num_hyphens,           
        num_at,                
        num_qmark,             
        num_and,               
        num_equals,            
        digits,                
        letters,                
        specials,               
        digit_ratio,            
        letter_ratio,           
        subdomains,             
        too_many_subdomains,    
        suspicious_subdomain,   
        is_https,               
        has_suspicious_word_overall, 
        has_suspicious_tld,     
        long_domain,            
        many_hyphens,           
        is_ip,                  
        entropy,                
        is_top_domain           
    ]