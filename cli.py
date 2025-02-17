#!/usr/bin/env python3

import argparse
import requests
import json

def create_json_file(date, filename):
    url = f'https://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-{date}.n.0/compose/metadata/rpms.json'
    local_filename = filename

    if not local_filename:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raises an HTTPError for bad responses (e.g., 404 or 500)
            with open(local_filename, 'wb') as file:
                # Write the file in chunks to avoid using too much memory
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive new chunks
                        file.write(chunk)
    return local_filename

def create_packages_list(filename):
    packages_list = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            packages = data["payload"]["rpms"]["Everything"]["x86_64"]
            for pack in packages:
                packages_list.append(pack)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    return packages_list

def find_common_packages(init_packages, final_packages):
    # Convert both lists to sets and compute their intersection.
    common_packages = list(set(init_packages) & set(final_packages))
    return common_packages


def find_removed_packages(init_packages, final_packages):
    # Removed packages are those present only in the init_packages
    nevra_names_init = []
    nevra_names_final = []

    for package in init_packages:
        nevra_names_init.append(package.rsplit("-", 2)[0])
    for package in final_packages:
        nevra_names_final.append(package.rsplit("-", 2)[0])

    # Convert both lists to sets and find the difference
    result = list(set(nevra_names_init) - set(nevra_names_final))

    for package_name in init_packages:
        for substring in result:
            if substring in package_name:
                print(f'{substring} REMOVED ({package_name})')

    return


def main():
    parser = argparse.ArgumentParser(description="A simple CLI example.")
    parser.add_argument("-i", "--initdate", type=str, help="The date to download the initial json file." )
    parser.add_argument("-f", "--finaldate", type=str, help="The date to download the final json file." )
    args = parser.parse_args()

    init_file = create_json_file(args.initdate, f"rpms_{args.initdate}.json")
    final_file = create_json_file(args.finaldate, f"rpms_{args.finaldate}.json")

    init_packages = create_packages_list(init_file)
    final_packages = create_packages_list(final_file)

    find_common_packages(init_packages, final_packages)
    find_removed_packages(init_packages, final_packages)

if __name__ == "__main__":
    main()
