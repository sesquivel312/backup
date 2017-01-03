#!/usr/bin/env python

import lib

args = lib.get_args()

type, source_path, dest_path, bkp_opts, reten_opts = lib.parse_config(args['config-file'])

lib.backup(source_path, dest_path, type=type, backup_opts=bkp_opts, retention_opts=reten_opts)