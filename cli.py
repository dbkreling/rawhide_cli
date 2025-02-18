#!/usr/bin/env python3

import os
import argparse
import requests
import json

def create_json_file(date, filename, batch):
    '''
    Creates a local json file based on the results of the server rpms.json for a specific date and return its name.

    Parameters:
        date (str): The name of the person to greet.
        filename (str): The name of the file to be created.
        batch (Optional[int]): An optional update batch. If not provided, defaults to "0".

    Returns:
        str: A filename.
    '''
    url = f'https://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-{date}.n.{batch}/compose/metadata/rpms.json'
    local_filename = filename

    if not os.path.isfile(local_filename):
        print(f"Creating file {local_filename}")

        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raises an HTTPError for bad responses (e.g., 404 or 500)
            with open(local_filename, 'wb') as file:
                # Write the file in chunks to avoid using too much memory
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    return local_filename

def create_packages_list(filename):
    '''
    Returns a list containing all x86_64 packages from a specific json file.

    Parameters:
        filename (str): The name of the file to be created.

    Returns:
        List[str]: A list of packages (packages_list).
    '''
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
    '''
    Returns a list of all x86_64 packages shared between two given packages lists.

    Parameters:
        init_packages (List[str]): list of packages from the initial date.
        final_packages (List[str]): list of packages from the final date.

    Returns:
        List[str]: A list of common packages between two files.
    '''
    # Convert both lists to sets and compute their intersection.
    common_packages = list(set(init_packages) & set(final_packages))
    return common_packages


def find_removed_packages(init_packages, final_packages):
    '''
    Prints and returns a list of all x86_64 packages removed from an initial list provided a final one.

    Parameters:
        init_packages (List[str]): list of packages from the initial date.
        final_packages (List[str]): list of packages from the final date.

    Returns:
        List[str]: A list of removed packages between two files.
    '''
    # Removed packages are those present only in the init_packages
    nevra_names_init = []
    nevra_names_final = []
    removed_packages = []

    nevra_names_init = [package.rsplit("-", 2)[0] for package in init_packages]
    nevra_names_final = [package.rsplit("-", 2)[0] for package in final_packages]

    # Convert both lists to sets and find the difference
    result = list(set(nevra_names_init) - set(nevra_names_final))

    for nevra_name in result:
        for package_name in init_packages:
            if nevra_name in package_name:
                removed_packages.append(package_name)
                print(f'{nevra_name} REMOVED ({package_name})')

    return removed_packages

def find_added_packages(init_packages, final_packages):
    '''
    Prints and returns a list of all x86_64 packages added to final list provided an initial one.

    Parameters:
        init_packages (List[str]): list of packages from the initial date.
        final_packages (List[str]): list of packages from the final date.

    Returns:
        List[str]: A list of added packages between two files.
    '''
    # Added packages are those present only in the final_packages
    nevra_names_init = []
    nevra_names_final = []
    added_packages = []

    nevra_names_init = [package.rsplit("-", 2)[0] for package in init_packages]
    nevra_names_final = [package.rsplit("-", 2)[0] for package in final_packages]

    # Convert both lists to sets and find the files only present in the final set
    result = list(set(nevra_names_final) - set(nevra_names_init))

    for nevra_name in result:
        for package_name in init_packages:
            if nevra_name in package_name:
                added_packages.append(package_name)
                print(f'{nevra_name} ADDED ({package_name})')

    return added_packages

def find_updated_packages(init_packages, final_packages):
    '''
    Prints a list of all x86_64 packages removed, added and updated in the final list compared to the initial one.

    Parameters:
        init_packages (List[str]): list of packages from the initial date.
        final_packages (List[str]): list of packages from the final date.

    Returns:
        List[str]: A list of updated packages between two files.
    '''
    stripped_init_packages = set(init_packages) - set(find_removed_packages(init_packages, final_packages))
    stripped_final_packages = set(final_packages) - set(find_added_packages(init_packages, final_packages))

    for init in sorted(list(stripped_init_packages)):
        for final in sorted(list(stripped_final_packages)):
            init_nevra_name = init.rsplit("-", 2)[0]
            final_nevra_name = final.rsplit("-", 2)[0]
            init_nevra_version = '-'.join(init.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
            final_nevra_version = '-'.join(final.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
            if init_nevra_name == final_nevra_name:
                if init_nevra_version != final_nevra_version:
                    print(f'{init_nevra_name} UPDATED ({init_nevra_version} -> {final_nevra_version})')
                    stripped_final_packages.remove(final)

    return

def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    parser.add_argument("-i", "--initdate", type=str, help="The date to download the initial json file." )
    parser.add_argument("-f", "--finaldate", type=str, help="The date to download the final json file." )
    parser.add_argument("-n", "--batchinit", type=int, default=0, help="The batch round of updates for multiple releases on the initial date.")
    parser.add_argument("-m", "--batchfinal", type=int, default=0, help="The batch round of updates for multiple releases on the final date.")
    args = parser.parse_args()

    init_file = create_json_file(args.initdate, f"rpms_{args.initdate}.json", args.batchinit)
    final_file = create_json_file(args.finaldate, f"rpms_{args.finaldate}.json", args.batchfinal)

    init_packages = create_packages_list(init_file)
    final_packages = create_packages_list(final_file)

    find_updated_packages(init_packages, final_packages)


if __name__ == "__main__":
    main()
