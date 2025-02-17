## Rawhide CLI

This code is a playground to play with the contents of https://kojipkgs.fedoraproject.org/compose/rawhide/

Usages:

## Print Rawhide compose updates (print_rawhide_composes.py):
```
usage: print_rawhide_composes.py [-h] {last,calc,all} ...

Manipulate metadata from Fedora's Rawhide and other time operations.

positional arguments:
  {last,calc,all}  Sub-command help
    last           Updates in the last X days
    calc           Calculate date X days before today
    all            Display all Rawhide updates

options:
  -h, --help       show this help message and exit
```

## CLI

```
usage: cli.py [-h] [-i INITDATE] [-f FINALDATE] [-n BATCHINIT] [-m BATCHFINAL]

A simple CLI tool.

options:
  -h, --help            show this help message and exit
  -i INITDATE, --initdate INITDATE
                        The date to download the initial json file.
  -f FINALDATE, --finaldate FINALDATE
                        The date to download the final json file.
  -n BATCHINIT, --batchinit BATCHINIT
                        The batch round of updates for multiple releases on the initial date.
  -m BATCHFINAL, --batchfinal BATCHFINAL
                        The batch round of updates for multiple releases on the final date.
```

### Example

```
./cli.py -i 20250203 -f 20250205 -m 3
```

In the command above, `-i` and `-f` are the initial and final dates where the cli will download the metadata from. The `-m` flag indicates that the final date has 4 updates (zero-indexed directories), and the user wants index number 3.

## Days Before today

```
usage: days_before.py [-h] days

Calculate the date X days before today.

positional arguments:
  days        Number of days before today

options:
  -h, --help  show this help message and exit
```

### Example

```
./days_before.py 5
```

## check_response_of_the_server.py

Simple tool used to verify the response of a server (currently hardcoded).