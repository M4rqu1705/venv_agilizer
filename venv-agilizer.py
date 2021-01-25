#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import venv

venv_directory = os.environ.get('VENV_DIR', os.getcwd())

#    _  _ ___ _    ___ ___ ___     ___ _   _ _  _  ___ _____ ___ ___  _  _ ___
#   | || | __| |  | _ \ __| _ \   | __| | | | \| |/ __|_   _|_ _/ _ \| \| / __|
#   | __ | _|| |__|  _/ _||   /   | _|| |_| | .` | (__  | |  | | (_) | .` \__ \
#   |_||_|___|____|_| |___|_|_\   |_|  \___/|_|\_|\___| |_| |___\___/|_|\_|___/
#
def env_locations():
    locations = dict()

    # Check in default directory
    for env in os.listdir(venv_directory):
        key = env
        value = os.path.join(venv_directory, key)
        locations[key] = value

    # Check in current working directory
    for entry in os.listdir():
        try:
            key = entry
            value = os.path.abspath(key)
            if os.path.isdir(key) and "Scripts" in os.listdir(value):
                locations[key] = value
        except PermissionError:
            continue

    return locations

def rmdir_recursive(target):
    for d in os.listdir(target):
        try:
            rmdir_recursive(os.path.join(target, d))
        except OSError:
            os.remove(os.path.join(target, d))
    os.rmdir(target)


#    _    ___ ___ _____
#   | |  |_ _/ __|_   _|
#   | |__ | |\__ \ | |
#   |____|___|___/ |_|
#
def list_available(args):
    print('Listing envs ...')
    locs = env_locations()

    # Print all with number
    for i, env in enumerate(locs):
        print(f'({i+1}) {env} in `{locs[env]}`')

#     ___ ___ ___   _ _____ ___
#    / __| _ \ __| /_\_   _| __|
#   | (__|   / _| / _ \| | | _|
#    \___|_|_\___/_/ \_\_| |___|
#
def create(args):
    env = args.env_name
    dir = args.dir
    ssp = args.ssp
    symlinks = args.sym
    clear = args.clear
    w_pip = args.wp
    prompt = args.prompt

    new_env = os.path.join(dir, env)

    venv.create(new_env,
            system_site_packages = ssp,
            clear=clear,
            symlinks=symlinks,
            with_pip=w_pip,
            prompt=prompt)

    if os.path.isdir(env_locations()[env]):
        print(f"[✓] `{env}` successfully created!")
    else:
        print(f'[✗] `{env}` was not successfully created.')

#    ___  ___ ___ _____ ___  _____   __
#   |   \| __/ __|_   _| _ \/ _ \ \ / /
#   | |) | _|\__ \ | | |   / (_) \ V /
#   |___/|___|___/ |_| |_|_\\___/ |_|
#
def destroy(args):
    env = args.env_name
    locs = env_locations()

    if env in locs:
        rmdir_recursive(locs[env])

    if not os.path.isdir(locs[env]) and not os.path.isfile(locs[env]):
        print(f'[✓] `{env}` successfully destroyed!')
    else:
        print(f'[✗] `{env}` could not be destroyed.')

#      _   ___ _____ _____   ___ _____ ___
#     /_\ / __|_   _|_ _\ \ / /_\_   _| __|
#    / _ \ (__  | |  | | \ V / _ \| | | _|
#   /_/ \_\___| |_| |___| \_/_/ \_\_| |___|
#
def activate(args):
    env = args.env_name
    locs = env_locations()

    if env in locs:
        activate_env = os.path.join(locs[env], 'Scripts', 'activate')
        os.system(f'doskey activate={activate_env}')

        print(f'[✓] Run `activate` to activate `{env}`')
    else:
        print(f'[✗] Could not activate inexistent `{env}`')


def main():
    parser = argparse.ArgumentParser(description='Make working with VENV and with default directory much easier')
    subparsers = parser.add_subparsers()


    #    _    ___ ___ _____
    #   | |  |_ _/ __|_   _|
    #   | |__ | |\__ \ | |
    #   |____|___|___/ |_|
    #
    parser_list = subparsers.add_parser(
            'list',
            help='List all available environments in default directory.')

    # Default function
    parser_list.set_defaults(func=list_available)


    #     ___ ___ ___   _ _____ ___
    #    / __| _ \ __| /_\_   _| __|
    #   | (__|   / _| / _ \| | | _|
    #    \___|_|_\___/_/ \_\_| |___|
    #
    parser_create = subparsers.add_parser(
            'create',
            help='Create new venv environment making sure to check if it already exists.')
    # Environment name
    parser_create.add_argument(
            'env_name',
            metavar='Environment Name',
            help='Indicates what is the name of the desired environment.')
    # Environment dir
    parser_create.add_argument(
            '-d',
            '--dir',
            metavar="Path to virtual environment",
            default=venv_directory,
            help='Specifies path to virutal environment.')
    # System site packages
    parser_create.add_argument(
            '--ssp',
            '--system-site-packages',
            action='store_true',
            help='Give the virtual environment access to the system site-packages directory.')
    # Symlinks
    parser_create.add_argument(
            '--sym',
            '--symlinks',
            action='store_true',
            help='Try to use symlinks rather than copies, when symlinks are not the default for the platform.')
    # Clear
    parser_create.add_argument(
            '-c',
            '--clear',
            action='store_true',
            help='Delete the contents of the environment directory if it already exists, before environment creation')
    # Without pip
    parser_create.add_argument(
            '--wp',
            '--without-pip',
            action='store_false',
            help='Skips installing or upgrading pip in the virtual environment')
    # Prompt
    parser_create.add_argument(
            '-p',
            '--prompt',
            metavar='Prompt',
            help='Provides an alternative prompt prefix to this environment')

    # Default function
    parser_create.set_defaults(func=create)


    #    ___  ___ ___ _____ ___  _____   __
    #   |   \| __/ __|_   _| _ \/ _ \ \ / /
    #   | |) | _|\__ \ | | |   / (_) \ V /
    #   |___/|___|___/ |_| |_|_\\___/ |_|
    #
    parser_destroy = subparsers.add_parser(
            'destroy',
            help='Destroy specified environment.')

    # Environment name
    parser_destroy.add_argument(
            'env_name',
            metavar='Environment Name',
            help='Indicates what is the name of the desired environment.')

    # Default function
    parser_destroy.set_defaults(func=destroy)


    #      _   ___ _____ _____   ___ _____ ___
    #     /_\ / __|_   _|_ _\ \ / /_\_   _| __|
    #    / _ \ (__  | |  | | \ V / _ \| | | _|
    #   /_/ \_\___| |_| |___| \_/_/ \_\_| |___|
    #
    parser_activate = subparsers.add_parser(
            'activate',
            help='Activate specified environment.')
    parser_activate.add_argument(
            'env_name',
            metavar='Environment Name',
            help='Indicates what is the name of the desired environment.')

    # Default function
    parser_activate.set_defaults(func=activate)



    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

# Thank you
# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/venv.html?highlight=venv#module-venv
# https://docs.python.org/2/library/os.path.html
