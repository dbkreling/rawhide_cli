#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta

def calculate_past_date(days):
    """Calculates the date X days before today."""
    past_date = datetime.today() - timedelta(days=days)
    return past_date.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD

def main():
    parser = argparse.ArgumentParser(description="Calculate the date X days before today.")
    parser.add_argument("days", type=int, help="Number of days before today")
    args = parser.parse_args()
    
    result_date = calculate_past_date(args.days)
    print(f"The date {args.days} days before today is: {result_date}")

if __name__ == "__main__":
    main()