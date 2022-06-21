#!/usr/bin/env python3

# Stanislas M. 2021-09-28

"""

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

csv = "site,score,security_headers_url\n"

# CHECKS

def export_to_csv():
    print("\nGenerated CSV: ./" + today + "-export.csv\n")
    f = open(today + "-export.csv", "a")
    f.write(csv)
    f.close()

# Core function

def scan(url):
    global csv

    site = url
    score = ""
    securityheaders_url = "https://securityheaders.com/?q=" + url + "&followRedirects=on"
    base_request = requests.get(securityheaders_url)

    if base_request.status_code == 200:
        base_text = base_request.text

        soup = BeautifulSoup(base_text, "html.parser")
        print("##", soup.title.string) 

        # score

        try: 
            score_div = soup.find_all("div", class_="score")
            score = re.search("[A-Z]", str(score_div[0])).group()
        except Exception: 
            score = "Unknown" 
            
        # CSV text
        csv += site + "," + score + "," + securityheaders_url + "\n"

        # Export
        export_to_csv()
        csv = ""

    else:
        raise Exception("HTTP error: " + str(base_request.status_code))

# URL -u / --url

def action_url(txt):
    print(txt)
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
    
