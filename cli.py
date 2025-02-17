#!/usr/bin/env python3

import os
import argparse
import requests
import json

def create_json_file(date, filename, batch):
    url = f'https://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-{date}.n.{batch}/compose/metadata/rpms.json'
    local_filename = filename

    if not os.path.isfile(local_filename):
        print(f"Creating file {local_filename}")

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

    for nevra_name in result:
        for package_name in init_packages:
            if nevra_name in package_name:
                print(f'{nevra_name} REMOVED ({package_name})')

    return

def find_added_packages(init_packages, final_packages):
    # Added packages are those present only in the final_packages
    nevra_names_init = []
    nevra_names_final = []

    for package in init_packages:
        nevra_names_init.append(package.rsplit("-", 2)[0])
    for package in final_packages:
        nevra_names_final.append(package.rsplit("-", 2)[0])

    # Convert both lists to sets and find the files only present in the final set
    result = list(set(nevra_names_final) - set(nevra_names_init))

    for nevra_name in result:
        for package_name in init_packages:
            if nevra_name in package_name:
                print(f'{nevra_name} ADDED ({package_name})')

    return


def main():
    parser = argparse.ArgumentParser(description="A simple CLI example.")
    parser.add_argument("-i", "--initdate", type=str, help="The date to download the initial json file." )
    parser.add_argument("-f", "--finaldate", type=str, help="The date to download the final json file." )
    parser.add_argument("-n", "--batchinit", type=int, default=0, help="The batch round of updates for multiple releases on the initial date.")
    parser.add_argument("-m", "--batchfinal", type=int, default=0, help="The batch round of updates for multiple releases on the final date.")
    args = parser.parse_args()

    init_file = create_json_file(args.initdate, f"rpms_{args.initdate}.json", args.batchinit)
    final_file = create_json_file(args.finaldate, f"rpms_{args.finaldate}.json", args.batchfinal)

    init_packages = create_packages_list(init_file)
    final_packages = create_packages_list(final_file)

    find_common_packages(init_packages, final_packages)
    find_removed_packages(init_packages, final_packages)
    find_added_packages(init_packages, final_packages)

if __name__ == "__main__":
    main()
