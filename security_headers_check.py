#!/usr/bin/env python3

# Stanislas M. 2022-06-20

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

# Current date

now = datetime.now()
today = now.strftime("%Y-%m-%d-%H_%M_%S")

# CSV

csv = "site,score,missing_headers,warnings,security_headers_url\n"

# CHECKS

# Credit: https://www.adamsmith.haus/python/answers/how-to-remove-empty-lines-from-a-string-in-python
def remove_empty_lines(txt):
    lines = txt.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in non_empty_lines:
      string_without_empty_lines += line + " - "
    return string_without_empty_lines

def export_to_csv():
    print("\nGenerated CSV: ./security-headers-" + today + "-export.csv\n")
    f = open("security-headers-" + today + "-export.csv", "a")
    f.write(csv)
    f.close()

# Core function

def scan(url):
    global csv

    site = url
    score = ""
    missing_headers = ""
    warnings = ""
    securityheaders_url = "https://securityheaders.com/?q=" + url + "&followRedirects=on"
    base_request = requests.get(securityheaders_url)

    if base_request.status_code == 200:
        base_text = base_request.text

        soup = BeautifulSoup(base_text, "html.parser")
        print("\nTitle: ", soup.title.string) 

        
        try:
            # score
            score_div = soup.find_all("div", class_="score")
            score = re.search("[A-Z]", str(score_div[0])).group()

            report_sections = soup.find_all("div", class_="reportSection")

            # missing headers
            missing_headers = remove_empty_lines(report_sections[3].get_text())

            # warnings
            warnings = remove_empty_lines(report_sections[4].get_text())

        except Exception: 
            score = "Unknown"
            missing_headers = "Unknown"
            warnings = "Unknown"

        print("Score: ", score)
        print("URL:   ", securityheaders_url)
        
        # debug - included in csv.
        # print(missing_headers)
        # print(warnings)
        
        # CSV text
        csv += site + "," + score + "," + missing_headers + "," + warnings + "," + securityheaders_url + "\n"

        # Export
        export_to_csv()
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
        print("General error : ", err) 
        exit(1)
    
