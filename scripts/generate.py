#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import datetime


def get_time():
    """
    Generate a formatted timestamp for currenttime
    """
    return str(datetime.datetime.now())


def get_autogen_header(path=None):
    file_path = os.path.join(path, "list_raw.txt")

    with open(file_path, "r") as f:
        data_version = f.readlines()[2]
        data_version = data_version[2:]
        data_version = data_version.rstrip()

        f.close()

    # Autogenerated header
    autogen_header = "This file was generated by The-Big-Username-Blacklist {} (at {})".format(  # NOQA
        data_version, get_time()
    )

    return autogen_header


def convert(path=None):
    """
    Loads data from list_raw and generates files in the following formats:
        - newline
        - json
        - python
        - js (ES5)
        - js (ES6)
        - php
    """
    # Load raw
    file_path = os.path.join(path, "list_raw.txt")

    with open(file_path, "r") as f:
        raw_usernames = f.readlines()

        # Remote newline
        usernames = [x.strip("\n") for x in raw_usernames]

        # Remove trailing #
        usernames = [x for x in usernames if x and not x.startswith("#")]

        # Sort list
        usernames.sort()

        f.close()

    # Write optimized newline file
    file_path = os.path.join(path, "list.txt")

    optimized_data = "".join("{}\n".format(e) for e in usernames)
    optimized_data = optimized_data.strip()

    autogen_header = get_autogen_header(path=path)

    with open(file_path, "w") as f:
        f.write(optimized_data)
        f.close()

    # Write optimized json file
    file_path = os.path.join(path, "list.json")

    with open(file_path, "w") as f:
        json.dump(usernames, f, indent=4, ensure_ascii=False)
        f.close()

    # Write python file
    file_path = os.path.join(path, "list.py")

    with open(file_path, "w") as f:
        f.write(f"# {autogen_header}\n")
        f.write(f"data = {usernames}")
        f.close()

    # Write es6 module
    file_path = os.path.join(path, "list.js")

    with open(file_path, "w") as f:
        f.write(f"// {autogen_header}\n")
        f.write(f"export default {usernames};")
        f.close()

    # Write commonjs module
    file_path = os.path.join(path, "list-commonjs.js")

    with open(file_path, "w") as f:
        f.write(f"// {autogen_header}\n")
        f.write(f"module.exports = {usernames};")
        f.close()

    # write PHP file
    file_path = os.path.join(path, "list.php")

    with open(file_path, "w") as f:
        f.write("<?php \n")
        f.write(f"// {autogen_header}\n")
        f.write(f"return {usernames};")
        f.close()

    # Write yaml file
    file_path = os.path.join(path, "list.yaml")

    with open(file_path, "w") as f:
        f.write(f"# {autogen_header}\n")
        f.write("---\n")
        f.write("usernames:\n")
        for username in usernames:
            f.write(f"  - \"{username}\"\n")
        f.close()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    list_dir = os.path.join(current_dir, os.pardir)

    convert(path=list_dir)
