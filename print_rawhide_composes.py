#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
from collections import Counter

from datetime import datetime, timedelta

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

def print_all_updates():
    print("Here's a list of Rawhide updates per day:" )
    for key,value in counter.items():
        if value == 1:
            singular_plural = "update"
        else:
            singular_plural = "updates"
        print(f"{value} {singular_plural} on {key}")


def calculate_past_date(days):
    """Calculates the date X days before today."""
    past_date = datetime.today() - timedelta(days=days)
    date = past_date.strftime("%Y-%m-%d")
    print(f"The date {days} days before today is: {date}")

    return


def number_of_updates_since_date(args_days):
    sliced_dict = dict(list(counter.items())[-args_days:])  # Get first 2 items
    number_of_rawhide_updates = sum(sliced_dict.values())

    print(f"In the last {args_days} days we had {number_of_rawhide_updates} Rawhide updates\n")
    print(f"Here's the list:")
    print(sliced_dict)

    return


def main():
    parser = argparse.ArgumentParser(description="Manipulate metadata from Fedora's Rawhide and other time operations.")

    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    add_parser = subparsers.add_parser('last', help="Updates in the last X days")
    add_parser.add_argument('days', type=int, help="Number of days ago to display the number of updates.")
    add_parser.set_defaults(func=lambda args: number_of_updates_since_date(args.days))

    add_parser = subparsers.add_parser('calc', help='Calculate date X days before today')
    add_parser.add_argument('days', type=int, help='Number of days to find the date')
    add_parser.set_defaults(func=lambda args: calculate_past_date(args.days))

    add_parser = subparsers.add_parser('all', help='Display all Rawhide updates')
    add_parser.set_defaults(func=lambda args: print_all_updates())

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
