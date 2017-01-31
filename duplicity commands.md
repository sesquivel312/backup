## This file lists the duplicity command lines, with options, useful for the backup wrapper

### Backup
[full] --archive-dir <archdir> --name <bkpname> <--no-compression> <--no-encryption> <backend><targetpath>

full will force a full, without the full option it will be an incremental - assuming there is an existing full

### Restore

### History Maintenance

duplicity remove-all-but-n-full <time> [options] --force <target-url>