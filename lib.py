#!/usr/bin/env python

import subprocess
import argparse
import ConfigParser
import sys


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', help='name of config file, including path as needed')
    args = parser.parse_args()

    return_args = {'config-file': args.config_file}

    if not return_args['config-file']:
        sys.exit('**Exiting, no config file provided**')

    return return_args


def parse_config(config_file):
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.read(config_file)

    section = config.sections()[0]  # for now this should contain only 1 item, future may allow multiple sections

    source_path = config.get(section, 'source-path')
    dest_path = config.get(section, 'dest-path')
    type = config.get(section, 'type')

    backup_opts = ['--archive-dir', config.get(section,'archive-dir'), '--name', section]

    if config.has_option(section, 'no-compression'):
        backup_opts.append('--no-compression')

    if config.has_option(section, 'no-encryption'):
        backup_opts.append('--no-encryption')

    retention_opts = [config.get(section,'retain-number'), '--archive-dir', config.get(section,'archive-dir'),
                      '--name', section, '--force']

    return type, source_path, dest_path, backup_opts, retention_opts


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