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

import unittest
import os
import os.path
import shutil

# ---- BEGIN Story ---
class TestDirectoryContents(unittest.TestCase):

    backup_dir = 'backups'
    daily_dir = 'daily'

    def setUp(self):
        files = os.listdir(self.backup_dir)
        [os.remove(os.path.join(self.backup_dir, file)) for file in files]

    # the backup directory ./backups is empty
    def test_backup_dir_empty(self):
        backup_dir = os.path.join(os.getcwd(), self.backup_dir)
        backup_dir_contents = os.listdir(backup_dir)
        self.assertTrue(len(backup_dir_contents) == 0)

    # this script is run manually from the CLI
    # the backup.conf file is provided via the --conf CLI argument
    def test_run_backup(self):
        # todo pickup here - run the backups using the CLI - which should fail b/c I've not implemented anything yet
        pass

    # the backup directory contains a full backup of the ./daily directory, i.e. ./backups/daily/...
    def test_backup_dir_has_backup(self):
        pass

    # the log file /var/log/duplicity.log contains ???
    # indicating a successful full backup of ./daily
    def test_backup_is_logged(self):
        pass

    # add more tests here (additional full backups for daily, check the directory, verify logs, verify deleted fulls, etc.)


if __name__ == '__main__':
    unittest.main()