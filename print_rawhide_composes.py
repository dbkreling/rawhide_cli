#!/usr/bin/env python3

import argparse
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

dates.pop(-1) # Removes a "Rawhide/" folder at the end of the list
counter = Counter(dates) # Create a dictionary with the counts for each date, sorted from the highest count

# print(dates)
# print()
# print(counter)

def print_all_updates():
def calculate_past_date(days):
    return

def number_of_updates_since_date(args_days):
    sliced_dict = dict(list(counter.items())[-args_days:])  # Get first 2 items
    number_of_rawhide_updates = sum(sliced_dict.values())

    print(f"In the last {args_days} we had {number_of_rawhide_updates} Rawhide updates\n")
    print(f"Here's the list:")
    print(sliced_dict)

    return

def main():
    parser = argparse.ArgumentParser(description="Calculate the date X days before today.")

    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    add_parser = subparsers.add_parser('last', help="Updates in the last X days")
    add_parser.add_argument('days', type=int, help="First number")
    add_parser.set_defaults(func=lambda args: number_of_updates_since_date(args.days))

    add_parser = subparsers.add_parser('calc', help='Calculate date X days before today')
    add_parser.add_argument('days', type=int, help='Number of days to find the date')
    add_parser.set_defaults(func=lambda args: calculate_past_date(args.days))

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
