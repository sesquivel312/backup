#!/usr/bin/env python

import ConfigParser
import argparse
import subprocess
import sys

from backup import Backup


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', help='name of config file, including path as needed')
    args = parser.parse_args()

    return_args = {'config-file': args.config_file}

    if not return_args['config-file']:
        sys.exit('**Exiting, no config file provided**')

    return return_args


def parse_config(config_file):
    """
    return a dictionary of backup objects

    dict is keyed by backup object's name attribute

    :param config_file: path to config file
    :return: dict of backup objects
    """
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.read(config_file)

    backups = {}

    for section in config.sections():

        curr_backup_name = config.get(section, 'name')
        curr_backup_init_values = {}

        for item in config.items(section):
            key = item[0]
            value = item[1]
            curr_backup_init_values[key] = value

        backups[curr_backup_name] = Backup(**curr_backup_init_values)


    return backups


def parse_output(output):
    # todo this will parse the output of duplicity command and add it to the logs
    pass


def backup(source_path, dest_path, type='full', backend='file://', backup_opts=[], retention_opts=[''], logger=None):
    """
    backup a directory or file using duplicity and options passed, also remove backups older that a given number

    this function also removes backups, specifically it keeps the n-most-recent backups, where n is the first item in
    the retention_options list (it MUST be included)

    Will execute full or incremental backup depending on the value of type (full, inc)
    :param source_path: string: what to backup
    :param dest_path: string: where to put the backup files
    :param type: string: {full, inc}
    :param backend: string: the 'URL Method' string for the backup backend - see the duplicity docs for details
    :param backup_opts: list: options passed to duplicity for backup
    :param retention_opts: list: options passed to duplicity when removing old backups
    :param logger: logger object: will handle logging
    :return:
    """

    # duplicity command would be (after duplicity)
    # full --archive-dir <archdir> --name <bkpname> <--no-compression> <--no-encryption> <backend><targetpath>
    # remove-all-but-n-full <#bkptokeep> --archive-dir <archdir> --name <bkpname> --force <backend><targetpath>

    # backup as directed
    if type == 'inc':
        command = ['duplicity']
    else:
        command = ['duplicity', type]
    command.extend(backup_opts)
    command.extend([source_path, backend + dest_path])

    output = subprocess.check_output(command)

    # todo parse and log output
    print output

    # remove backups as directed
    command = ['duplicity', 'remove-all-but-n-full']
    command.extend(retention_opts)
    command.extend([backend + dest_path])

    output = subprocess.check_output(command)

    # todo parse and log output
    print output


def restore(archive_path, restore_path, backend='file://', restore_opts=[], logger=None):
    pass  # todo construct a wrapper for 'duplicity [restore]'