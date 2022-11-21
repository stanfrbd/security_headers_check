#!/usr/bin/env python3

# Stanislas M. 2022-11-09

"""
usage: security_headers_check.py [-h] [-u URL] [-i INPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     http://example.com -- it will export to csv in the current directory
  -i INPUT_FILE, --input-file INPUT_FILE
                        Choose the path to input file containing URLs e.g. "test.txt" -- it will export to csv in the
                        current directory
"""

import json
import argparse
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

# CSV separator
SEP = ","

# Your proxy here...
proxy = ""

# Current date
now = datetime.now()
today = now.strftime("%Y-%m-%d-%H_%M_%S")

# Required Headers
"""
| Required HTTP 1.1 (HTTPS):     |
| ------------------------------ |
| Content-Security-Policy        |
| HTTP Strict-Transport-Security |
| X-Content-Type-Options         |
| Cache-Control                  |

| Required HTTP 1.0 (HTTPS):     |
| ------------------------------ |
| Content-Security-Policy        |
| HTTP Strict-Transport-Security |
| X-Content-Type-Options         |
| Expires                        |
"""

REQUIRED_HEADERS_HTTP_10_OR_11 = [ "Cache-Control", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options", "Expires" ]

# Optional Headers
"""
| Header                      | HTTP Versions       |
| --------------------------- | ------------------- |
| Access-Control-Allow-Origin | HTTP/1.0 / HTTP/1.1 |
| Location                    | HTTP/1.0 / HTTP/1.1 |
| Set-Cookie                  | HTTP/1.0 / HTTP/1.1 |
| WWW-Authenticate            | HTTP/1.0 / HTTP/1.1 |
| X-Frame-Options             | HTTP/1.0 / HTTP/1.1 |
| X-XSS-Protection            | HTTP/1.0 / HTTP/1.1 |
| Permissions-Policy          | HTTP/1.0 / HTTP/1.1 |
| Referrer-Policy             | HTTP/1.0 / HTTP/1.1 |
"""

OPTIONAL_HEADERS = [ "Access-Control-Allow-Origin", "Location", "Set-Cookie", "WWW-Authenticate", "X-Frame-Options", "X-XSS-Protection", "Permissions-Policy", "Referrer-Policy" ]

# CSV Headers
csv = "site" + SEP + "score" + SEP + "httpforwarding" + SEP + "missing_required_headers" + SEP + "missing_optional_headers" + SEP + "warnings" + SEP + "security_headers_url" + "\n"

# CHECKS

# Credit: https://www.adamsmith.haus/python/answers/how-to-remove-empty-lines-from-a-string-in-python
def remove_empty_lines(txt):
    lines = txt.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in non_empty_lines:
      string_without_empty_lines += line.replace(";", " ") + " - "
    return string_without_empty_lines.replace(",", " ")

def export_to_csv():
    print("\nGenerated CSV: ./security-headers-" + today + "-export.csv\n")
    f = open("security-headers-" + today + "-export.csv", "a")
    f.write(csv)
    f.close()

def check_missing_required_headers(txt):
    missing_found = False
    found_missing_required_headers = ""
    for el in REQUIRED_HEADERS_HTTP_10_OR_11:
        if el in txt:
            missing_found = True
            found_missing_required_headers += el + " | "
    if missing_found == False:
        return "No issue"
    return found_missing_required_headers

def check_missing_optional_headers(txt):
    missing_found = False
    found_missing_optional_headers = ""
    for el in OPTIONAL_HEADERS:
        if el in txt:
            missing_found = True
            found_missing_optional_headers +=  el + " | "
    if missing_found == False:
        return "No issue"        
    return found_missing_optional_headers

def check_http_forwarding(url):
    try:
        proxy_servers = { 'http': proxy, 'https': proxy }
        if "http" not in url:
            url = "https://" + url
        response = requests.get(url, timeout=10, proxies=proxy_servers)
    except:
        return "Unreachable"
	
    try:
        if response.history:
            if len(response.history) == 1:
                # Redirect URL
                return response.url
            else:
                # Last forwarding URL
                return response.history[len(response.history) - 1].url
        else:
            return "No forwarding"
    except:
        return "Unknown"

# CORE FUNCTION

def scan(url):
    global csv

    proxy_servers = { 'http': proxy, 'https': proxy }

    site = url
    score = ""
    httpforwarding = ""
    missing_req_headers = ""
    missing_opt_headers = ""
    warnings = ""
    securityheaders_url = "https://securityheaders.com/?q=" + url + "&followRedirects=on"
    base_request = requests.get(securityheaders_url, proxies=proxy_servers)

    if base_request.status_code == 200:
        base_text = base_request.text

        soup = BeautifulSoup(base_text, "html.parser")
        print("\nTitle: ", soup.title.string) 

        # https://securityheaders.com
        try:
            # Score
            score_div = soup.find_all("div", class_="score")
            score = re.search("[A-Z]", str(score_div[0])).group()

            # Dividing content in sections
            report_sections = soup.find_all("div", class_="reportSection")

            # Missing Headers or Warnings
            extracted_data3 = remove_empty_lines(report_sections[3].get_text())
            if "Missing Headers" in extracted_data3:
                missing_req_headers = check_missing_required_headers(extracted_data3)
                missing_opt_headers = check_missing_optional_headers(extracted_data3)
            elif "Warnings" in extracted_data3:
                warnings = extracted_data3
                missing_req_headers = "No issue"
                missing_opt_headers = "No issue"

            # Warnings if exist
            extracted_data4 = remove_empty_lines(report_sections[4].get_text())
            if "Warnings" in extracted_data4:
                warnings = extracted_data4
            else:
                warnings = ""

        except Exception: 
            score = "Unknown"
            missing_req_headers = "Unknown"
            missing_opt_headers = "Unknown"
            warnings = "Unknown"

        # HTTP Forwarding
        httpforwarding = check_http_forwarding(url)

        print("Score: ", score)
        print("URL:   ", securityheaders_url)
        print("HTTP Forwarding: ", httpforwarding)
        
        # CSV text
        csv += site + SEP + score + SEP + httpforwarding + SEP + missing_req_headers + SEP + missing_opt_headers + SEP + warnings + SEP + securityheaders_url + "\n"

        # Export
        export_to_csv()

        # clear variables
        csv = ""

    else:
        raise Exception("HTTP error: " + str(base_request.status_code))

# URL -u / --url

def action_url(txt):
    print("# ", txt)
    scan(txt)

# INPUT_FILE -i / --input-file

def action_file(txt):
    if Path(txt).is_file():
        input_file = open(txt, "r")
        data = input_file.readlines()
        input_file.close()
        if data != []:
            for i in range (0, len(data)):
                action_url(data[i].rstrip('\n'))
    else:
        print("\"" + txt + "\" is not a valid file, aborting.")

# MAIN

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url', help='http://example.com -- it will export to csv in the current directory')
    parser.add_argument('-i','--input-file', help='Choose the path to input file containing URLs e.g. "test.txt" -- it will export to csv in the current directory')
    
    global args
    args = parser.parse_args()

    if args.url:
        action_url(args.url)

    if args.input_file:
        action_file(args.input_file)    

if __name__ == "__main__":
    try: 
        main() 
    except Exception as err: 
        print("General error: ", err) 
        exit(1)
