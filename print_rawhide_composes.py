#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

# URL of the directory listing
url = "https://kojipkgs.fedoraproject.org/compose/rawhide/"

# Fetch the webpage
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch page")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")
update_count_per_day=1
update_date=0
last_update_date=0

# Extract links (assuming directory listings are hyperlinks)
for link in soup.find_all("a"):
    href = link.get("href")
    if href and not href.startswith("?") and not href.startswith("/"):
        update_date=(href.split("-", 3)[2]).split(".")[0]

        if last_update_date == update_date:
            update_count_per_day+=1
        else:
            update_count_per_day=1

        last_update_date=update_date

        print(last_update_date, update_count_per_day)

print(f"Date {update_date} had {update_count_per_day} updates")        # print(href)  # Print directory/file names