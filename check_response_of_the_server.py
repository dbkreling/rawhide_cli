#!/usr/bin/env python3

import requests

url = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
response = requests.get(url)

content_type = response.headers.get("Content-Type", "")
print(f"Content-Type: {content_type}")