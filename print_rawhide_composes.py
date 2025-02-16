#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from collections import Counter

# URL of the directory listing
url = "https://kojipkgs.fedoraproject.org/compose/rawhide/"

# Fetch the webpage
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch page")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")
dates = []
# Extract links (assuming directory listings are hyperlinks)
for link in soup.find_all("a"):
    href = link.get("href")
    if href and not href.startswith("?") and not href.startswith("/"):
        date = (href.split("-", 3)[2]).split(".")[0]
        dates.append(date)

dates.pop(-1)
counter = Counter(dates)

# print(dates)

# print(counter)
print("Here's a list of Rawhide updates per day:" )
for key,value in counter.items():
    if value == 1:
        singular_plural = "update"
    else:
        singular_plural = "updates"
    print(f"{value} {singular_plural} on {key}")
