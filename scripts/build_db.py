# Copyright 2018 Jose Cambronero and Phillip Stanley-Marbell
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from argparse import ArgumentParser
import os
import subprocess
import sys

from specimen.database import db as db_def
from specimen.database import parsers
from specimen.database.dbtypes import *


def create_db(name):
    pass
    # subprocess.call(['psql', '-c', 'CREATE DATABASE %s' % name])
    # subprocess.call(['psql', '-c', "ALTER DATABASE %s SET log_statement='none'" % name])

def populate(db_name, data_dir, bufferSize, cacheLimit):
    print "Parsing files in directory %s " % data_dir
    print "Writing to Database(%s) with buffer limit = %s and cache limit = %s" % (db_name, bufferSize, cacheLimit)

    rectypes = [User, Device, Carrier, Session, Event, SelectionEvent, PurchaseEvent, LevelEvent]
    try:
        db = db_def.Database(db_name, rectypes, bufferSize, cacheLimit)
    except Exception as e:
        import pdb
        pdb.post_mortem()
    # try to create tables if hasn't happened yet
    try:
        db.create_tables()
    except:
        pass

    jsonparser = parsers.JsonSpecimenParser(db)
    csvparser = parsers.CsvSpecimenParser(db)

    file_names = os.listdir(data_dir)

    if len(file_names) >= 5:
        # if we are parsing in a lot of data, better off dropping indices
        # and rebuilding later
        db.drop_indices()

    for file_name in file_names:
        ending = file_name.split(".")[-1]
        full_file_name = os.path.abspath(os.path.join(data_dir, file_name))
        try:
            if ending == file_name:
                ValueError("%s file missing ending" % full_file_name)
            elif ending == "json":
                jsonparser.parse(full_file_name)
            elif ending == "csv":
                csvparser.parse(full_file_name)
            else:
                print "Unable to parse files with ending: %s (%s)" % (ending, full_file_name)
        except Exception as e:
            print "==> Failed to parse %s" % full_file_name
            print e.message
            # start fresh for next file
            db.clear()

    # try creating indices if necessary
    db.create_indices()
    # recalculate database stats
    db.build_stats()
    # remove duplicate records and sessions
    # db.remove_duplicate_sessions()

def main(data_dir, db_name, _buffer, cache):
    create_db(db_name)
    populate(db_name, data_dir, _buffer, cache)

if __name__ == "__main__":
    argparser = ArgumentParser(description='Populates specimen database from directory of raw json/csv Specimen data files')
    argparser.add_argument('data_dir', help='Directory with json/csv files to use for population')
    argparser.add_argument('db_name', help='Postgres database name (created if it doesnt exist)')
    argparser.add_argument('--buffer', type=int, help='Buffer size in number of records', default=20000)
    argparser.add_argument('--cache', type=int, help='Cache limit for keeping in-memory foreign key references', default=40000)
    args = argparser.parse_args()
    main(args.data_dir, args.db_name, args.buffer, args.cache)