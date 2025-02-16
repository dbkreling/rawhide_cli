#!/usr/bin/env python3

import argparse
import requests
import json

def create_json_file(date, filename):
    url = f'https://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-{date}.n.0/compose/metadata/rpms.json'
    local_filename = filename

    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Raises an HTTPError for bad responses (e.g., 404 or 500)
        with open(local_filename, 'wb') as file:
            # Write the file in chunks to avoid using too much memory
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
    return local_filename

def main():
    parser = argparse.ArgumentParser(description="A simple CLI example.")
    parser.add_argument("-i", "--initdate", type=str, help="The date to download the initial json file." )
    parser.add_argument("-f", "--finaldate", type=str, help="The date to download the final json file." )
    args = parser.parse_args()

    create_json_file(args.initdate, f"rpms_{args.initdate}.json")
    create_json_file(args.finaldate, f"rpms_{args.finaldate}.json")

    try:
        with open(args.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            # print(data)
        with open("output.json", "w", encoding="utf-8") as fileo:
            json.dump(data, fileo, indent=4)
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Output file output.json created.")

if __name__ == "__main__":
    main()
