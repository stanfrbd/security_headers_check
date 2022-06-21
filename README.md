# security_headers_check

## Install dependencies

```
pip install -r requirements.txt
```

## Usage

```
usage: security_headers_check.py [-h] [-u URL] [-i INPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     http://example.com -- it will export to csv in the current directory
  -i INPUT_FILE, --input-file INPUT_FILE
                        Choose the path to input file containing URLs e.g. "test.txt" -- it will export to csv in the
                        current directory
```

## Using a single domain

```
python3 security_headers_check.py -u example.com
```

## Using a file containing domains

```
python3 security_headers_check.py -i sample.txt
```

## Content of sample.txt

```
duckduckgo.com
google.com
facebook.com
example.com
toto.com
```

## Result of execution

```
#  duckduckgo.com

Title:  Scan results for duckduckgo.com
Score:  A
URL:    https://securityheaders.com/?q=duckduckgo.com&followRedirects=on

Generated CSV: ./2022-06-21-09_14_17-export.csv

#  google.com

Title:  Scan results for google.com
Score:  F
URL:    https://securityheaders.com/?q=google.com&followRedirects=on

Generated CSV: ./2022-06-21-09_14_17-export.csv

#  facebook.com

Title:  Scan results for facebook.com
Score:  A
URL:    https://securityheaders.com/?q=facebook.com&followRedirects=on

Generated CSV: ./2022-06-21-09_14_17-export.csv

#  example.com

Title:  Scan results for example.com
Score:  F
URL:    https://securityheaders.com/?q=example.com&followRedirects=on

Generated CSV: ./2022-06-21-09_14_17-export.csv

#  toto.com

Title:  Scan results for toto.com
Score:  Unknown
URL:    https://securityheaders.com/?q=toto.com&followRedirects=on

Generated CSV: ./2022-06-21-09_14_17-export.csv
```

Since `toto.com` is not available for scanning, we don't know its score.
