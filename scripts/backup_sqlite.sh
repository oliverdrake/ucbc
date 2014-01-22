#!/bin/bash
cd ~/sites/ucbc/ucbc
backup_file="/tmp/sqlite3_dump_$(date --utc +%FT%T).bak"
sqlite3 db.sqlite3 .dump > $backup_file
boto-rsync -a key -s secret $backup_file s3://ucbcbackups/
