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
toto.cuik
```

## Result of execution

```
#  duckduckgo.com

Title:  Scan results for duckduckgo.com
Score:  A
URL:    https://securityheaders.com/?q=duckduckgo.com&followRedirects=on
HTTP Forwarding:  No forwarding

Generated CSV: ./security-headers-2022-11-09-16_55_14-export.csv

#  google.com

Title:  Scan results for google.com
Score:  D
URL:    https://securityheaders.com/?q=google.com&followRedirects=on
HTTP Forwarding:  https://www.google.com/

Generated CSV: ./security-headers-2022-11-09-16_55_14-export.csv

#  facebook.com

Title:  Scan results for facebook.com
Score:  A
URL:    https://securityheaders.com/?q=facebook.com&followRedirects=on
HTTP Forwarding:  https://www.facebook.com/

Generated CSV: ./security-headers-2022-11-09-16_55_14-export.csv

#  example.com

Title:  Scan results for example.com
Score:  F
URL:    https://securityheaders.com/?q=example.com&followRedirects=on
HTTP Forwarding:  No forwarding

Generated CSV: ./security-headers-2022-11-09-16_55_14-export.csv

#  toto.cuik

Title:  Scan results for toto.cuik
Score:  Unknown
URL:    https://securityheaders.com/?q=toto.cuik&followRedirects=on
HTTP Forwarding:  Unreachable

Generated CSV: ./security-headers-2022-11-09-16_55_14-export.csv
```

Since `toto.cuik` is not available for scanning, we don't know its score.

## Content of the CSV

```
site,score,httpforwarding,missing_required_headers,missing_optional_headers,warnings,security_headers_url
duckduckgo.com,A,No forwarding,No issue,No issue,,https://securityheaders.com/?q=duckduckgo.com&followRedirects=on
google.com,D,https://www.google.com/,Content-Security-Policy | X-Content-Type-Options | ,Permissions-Policy | Referrer-Policy | ,,https://securityheaders.com/?q=google.com&followRedirects=on
facebook.com,A,https://www.facebook.com/,No issue,Permissions-Policy | Referrer-Policy | ,Warnings - Content-Security-PolicyThis policy contains 'unsafe-inline' which is dangerous in the default-src directive. This policy contains 'unsafe-eval' which is dangerous in the default-src directive. This policy contains 'unsafe-inline' which is dangerous in the script-src directive. This policy contains 'unsafe-eval' which is dangerous in the script-src directive. This policy contains 'unsafe-inline' which is dangerous in the style-src directive.   - ,https://securityheaders.com/?q=facebook.com&followRedirects=on
example.com,F,No forwarding,Content-Security-Policy | X-Content-Type-Options | ,X-Frame-Options | Permissions-Policy | Referrer-Policy | ,Warnings - Site is using HTTPThis site was served over HTTP and did not redirect to HTTPS.  - ,https://securityheaders.com/?q=example.com&followRedirects=on
toto.cuik,Unknown,Unreachable,Unknown,Unknown,Unknown,https://securityheaders.com/?q=toto.cuik&followRedirects=on
```
