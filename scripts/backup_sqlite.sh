#!/bin/bash
cd ~/sites/ucbc/ucbc
backup_file="/tmp/sqlite3_dump_$(date --utc +%FT%T).bak"
sqlite3 db.sqlite3 .dump > $backup_file
boto-rsync -a AKIAJ4F55224DJHO4IOA -s n1q/IUsqFORjA/GLuZmGLJibegKcKyC5zJi5eZ3f $backup_file s3://ucbcbackups/
