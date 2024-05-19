import requests
from bs4 import BeautifulSoup
import subprocess

# Function to check for SQL Injection vulnerability
def sql_injection_scan(url):
    print("[*] Starting SQL Injection Scan...")
    result = subprocess.run(['sqlmap', '-u', url, '--batch', '--crawl=1'], capture_output=True, text=True)
    if 'all tested parameters appear to be not injectable' in result.stdout:
        print("[+] No SQL Injection vulnerability found.")
    else:
        print("[!] SQL Injection vulnerability detected!")
        print(result.stdout)

# Function to check for XSS vulnerability
def xss_scan(url):
    print("[*] Starting XSS Scan...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')
    
    xss_payload = "<script>alert('XSS')</script>"
    for form in forms:
        action = form.get('action')
        post_url = url if not action else action
        inputs = form.find_all('input')
        
        data = {}
        for input_tag in inputs:
            name = input_tag.get('name')
            type = input_tag.get('type')
            value = input_tag.get('value')
            
            if type == 'text':
                value = xss_payload
            
            data[name] = value
        
        response = requests.post(post_url, data=data)
        if xss_payload in response.text:
            print(f"[!] XSS vulnerability detected in form: {form}")
        else:
            print("[+] No XSS vulnerability found in form.")

# Function to run nmap scan for open ports
def nmap_scan(target):
    print("[*] Starting Nmap Scan...")
    result = subprocess.run(['nmap', '-sV', target], capture_output=True, text=True)
    print(result.stdout)

# Main function
def main():
    url = input("Enter the URL to scan: ")
    target = input("Enter the target for Nmap scan (IP or domain): ")

    sql_injection_scan(url)
    xss_scan(url)
    nmap_scan(target)

if __name__ == "__main__":
    main()
