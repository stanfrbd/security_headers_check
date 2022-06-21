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

Generated CSV: ./security-headers-2022-06-21-10_44_41-export.csv

#  google.com

Title:  Scan results for google.com
Score:  D
URL:    https://securityheaders.com/?q=google.com&followRedirects=on

Generated CSV: ./security-headers-2022-06-21-10_44_41-export.csv

#  facebook.com

Title:  Scan results for facebook.com
Score:  A
URL:    https://securityheaders.com/?q=facebook.com&followRedirects=on

Generated CSV: ./security-headers-2022-06-21-10_44_41-export.csv

#  example.com

Title:  Scan results for example.com
Score:  F
URL:    https://securityheaders.com/?q=example.com&followRedirects=on

Generated CSV: ./security-headers-2022-06-21-10_44_41-export.csv

#  toto.com

Title:  Scan results for toto.com
Score:  Unknown
URL:    https://securityheaders.com/?q=toto.com&followRedirects=on

Generated CSV: ./security-headers-2022-06-21-10_44_41-export.csv
```

Since `toto.com` is not available for scanning, we don't know its score.

## Content of the CSV

```
site,score,missing_headers,warnings,security_headers_url
duckduckgo.com,A,Warnings - Content-Security-PolicyThis policy contains 'unsafe-inline' which is dangerous in the script-src directive. This policy contains 'unsafe-eval' which is dangerous in the script-src directive. This policy contains 'unsafe-inline' which is dangerous in the style-src directive. Referrer-PolicyThe "origin" value is not recommended.   - ,Upcoming Headers - Cross-Origin-Embedder-PolicyCross-Origin Embedder Policy allows a site to prevent assets being loaded that do not grant permission to load them via CORS or CORP.Cross-Origin-Opener-PolicyCross-Origin Opener Policy allows a site to opt-in to Cross-Origin Isolation in the browser.Cross-Origin-Resource-PolicyCross-Origin Resource Policy allows a resource owner to specify who can load the resource.  - ,https://securityheaders.com/?q=duckduckgo.com&followRedirects=on
google.com,D,Missing Headers - Content-Security-PolicyContent Security Policy is an effective measure to protect your site from XSS attacks. By whitelisting sources of approved content, you can prevent the browser from loading malicious assets.X-Content-Type-OptionsX-Content-Type-Options stops a browser from trying to MIME-sniff the content type and forces it to stick with the declared content-type. The only valid value for this header is "X-Content-Type-Options: nosniff".Referrer-PolicyReferrer Policy is a new header that allows a site to control how much information the browser includes with navigations away from a document and should be set by all sites.Permissions-PolicyPermissions Policy is a new header that allows a site to control which features and APIs can be used in the browser.  - ,Upcoming Headers - Expect-CTExpect-CT allows a site to determine if they are ready for the upcoming Chrome requirements and/or enforce their CT policy.Cross-Origin-Embedder-PolicyCross-Origin Embedder Policy allows a site to prevent assets being loaded that do not grant permission to load them via CORS or CORP.Cross-Origin-Opener-PolicyCross-Origin Opener Policy allows a site to opt-in to Cross-Origin Isolation in the browser.Cross-Origin-Resource-PolicyCross-Origin Resource Policy allows a resource owner to specify who can load the resource.  - ,https://securityheaders.com/?q=google.com&followRedirects=on
facebook.com,A,Missing Headers - Referrer-PolicyReferrer Policy is a new header that allows a site to control how much information the browser includes with navigations away from a document and should be set by all sites.Permissions-PolicyPermissions Policy is a new header that allows a site to control which features and APIs can be used in the browser.  - ,Warnings - Content-Security-PolicyThis policy contains 'unsafe-inline' which is dangerous in the default-src directive. This policy contains 'unsafe-eval' which is dangerous in the default-src directive. This policy contains 'unsafe-inline' which is dangerous in the script-src directive. This policy contains 'unsafe-eval' which is dangerous in the script-src directive. This policy contains 'unsafe-inline' which is dangerous in the style-src directive.   - ,https://securityheaders.com/?q=facebook.com&followRedirects=on
example.com,F,Missing Headers - Content-Security-PolicyContent Security Policy is an effective measure to protect your site from XSS attacks. By whitelisting sources of approved content, you can prevent the browser from loading malicious assets.X-Frame-OptionsX-Frame-Options tells the browser whether you want to allow your site to be framed or not. By preventing a browser from framing your site you can defend against attacks like clickjacking. Recommended value "X-Frame-Options: SAMEORIGIN". X-Content-Type-OptionsX-Content-Type-Options stops a browser from trying to MIME-sniff the content type and forces it to stick with the declared content-type. The only valid value for this header is "X-Content-Type-Options: nosniff".Referrer-PolicyReferrer Policy is a new header that allows a site to control how much information the browser includes with navigations away from a document and should be set by all sites.Permissions-PolicyPermissions Policy is a new header that allows a site to control which features and APIs can be used in the browser.  - ,Warnings - Site is using HTTPThis site was served over HTTP and did not redirect to HTTPS.  - ,https://securityheaders.com/?q=example.com&followRedirects=on
toto.com,Unknown,Unknown,Unknown,https://securityheaders.com/?q=toto.com&followRedirects=on
```
