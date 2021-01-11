#!/usr/bin/python3

import argparse
import pycurl
from io import BytesIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a GPX file from OS Maps")
    parser.add_argument('firefox_curl_file', metavar='C', type=str, help='Firefox curl command as a text file')
    parser.add_argument('walk_id', metavar='C', type=str, help='Walk ID (https://osmaps.ordnancesurvey.co.uk/route/[ID]/export.gpx)')
    args = parser.parse_args()
    str = get_gpx(args.firefox_curl_file, args.walk_id)
    print(str)

def get_gpx(firefox_curl_file, walk_id):
    extra_headers = []
    with open(firefox_curl_file) as f:
        cmd = f.read()
        tokens = cmd.split("-H")
        for i in range(0, len(tokens)):
                # The trailing photo has a newline
                tokens[i] = tokens[i].rstrip("\n")
                # All the tokens are extra headers except for a rogue --compressed!
                tokens[i] = tokens[i].replace('--compressed', '')
                # Remove the leading and trailing ' symbols that are included on each extra header
                tokens[i] = tokens[i].lstrip(' \'')
                tokens[i] = tokens[i].rstrip(' \'')
        extra_headers = tokens[1:]

    url = 'https://osmaps.ordnancesurvey.co.uk/route/'+walk_id+'/export.gpx'

    # Similar to example at http://pycurl.io/docs/latest/quickstart.html
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, extra_headers)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return body.decode('utf-8')
