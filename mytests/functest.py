# objective is to backup files in the following directories
# ./daily (call this backup daily)
# ./weekly (backup weekly)
# ./bi-weekly (backup biweekly)

# backup daily:
#  name = daily
#  method = file  << maps to duplicity back-end
#  src = ./daily/
#  dst = ./backups/daily/
#  do not encrypt or compress files
#  full every week, incremental all other times
#  keep at most 3 full backups - including this one

# backup weekly
#  name = weekly
#  method = file  << maps to duplicity back-end
#  src = ./weekly/
#  dst = ./backups/weekly/
#  encrypt AND compress files
#  full every 4th backup, incremental all other times
#  keep at most 2 full backups - including this one

# backup biweekly
#  name = biweekly
#  method = file  << maps to duplicity back-end
#  src = ./biweekly/
#  dst = ./backups/biweekly/
#  do not encrypt files
#  do compress files
#  full every 4th backup, incremental all other times
#  keep at most 2 full backups - including this one

from __future__ import absolute_import

import ConfigParser
import os
import os.path
import shutil
import unittest

from backup import lib


# ---- BEGIN Story ---


class TestDirectoryContents(unittest.TestCase):

    test_config_file = '/home/steve/dev/backup/mytests/mytests.conf'
    test_config_global_section_name = 'Global'
    backup_config_file = '/home/steve/dev/backup/backup.conf'

    def setUp(self):

        testconfig = ConfigParser.RawConfigParser()
        testconfig.read(self.test_config_file)

        # delete the entire backup target directory and all it's contents - recursively
        self.backup_base_dir = testconfig.get(self.test_config_global_section_name, 'backup_base_dir')
        shutil.rmtree(self.backup_base_dir)

        # recreate the backup directory
        os.mkdir(self.backup_base_dir)

    # there's a valid backup config file
    def test_backup_conf_valid(self):

        backupconfig = ConfigParser.RawConfigParser()
        backupconfig.read(self.backup_config_file)
        self.assertGreater(len(backupconfig.items('daily')), 0)
        # verify the source directory in the backup.conf file
        source_dir = backupconfig.get('daily','source')
        self.assertTrue(os.path.exists(source_dir))

    # the backup directory is empty
    def test_backup_dir_empty(self):
        backup_dir = os.path.join(os.getcwd(), self.backup_base_dir)
        backup_dir_contents = os.listdir(backup_dir)
        self.assertTrue(len(backup_dir_contents) == 0)

    # this script is run manually from the CLI
    # the backup.conf file is provided via the --conf CLI argument
    def test_parse_backup_config(self):

        # parsing the config should return backups, one per section
        # verify the 'checkme' config is parsed properly
        # the config parser should return:
        # name: daily, method: file, source and destination params, compress =
        # encrypt = no, full= 7, keep = 3

        backups = lib.parse_config(self.backup_config_file)

        print backups

        checkme = backups['checkme']  # returns a dict of backup objects

        # todo add descriptive assert fail messages
        self.assertEqual(checkme.name, 'checkme')
        self.assertEqual(checkme.method, 'file')
        self.assertEqual(checkme.source, '/home/steve/dev/backup/origin/daily')
        self.assertEqual(checkme.destination, '/home/steve/dev/backup/dest/daily')
        self.assertEqual(checkme.compress, 'on')
        self.assertEqual(checkme.encrypt, 'on')
        self.assertEqual(checkme.full, '7')
        self.assertEqual(checkme.keep, '3')


    def test_run_backup(self):
        # todo next test to write
        pass


    # the backup directory contains a full backup of the ./daily directory, i.e. ./backups/daily/...
    def test_backup_dir_has_backup(self):
        pass

    # the log file /var/log/duplicity.log contains ???
    # indicating a successful full backup of ./daily
    def test_backup_is_logged(self):
        pass

    # add more mytests here (additional full backups for daily, check the directory, verify logs, verify deleted fulls, etc.)


if __name__ == '__main__':
    unittest.main()