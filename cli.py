#!/usr/bin/env python3

import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="A simple CLI example.")
    parser.add_argument("-f", "--filename", type=str, help="Name of the file to be parsed.", default="rpms.json")
    args = parser.parse_args()
    
    print(f"Parsing file.... {args.filename}")

    try:
        with open(args.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(data)
        with open("output.json", "w", encoding="utf-8") as fileo:
            json.dump(data, fileo, indent=4)
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()