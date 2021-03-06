#!/usr/bin/python
""" 
A simple file renaming application for easy photo organisation

Copyright (C) 2012 - Paul Pritchard

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>."""

import sys
import argparse
import os
import mimetypes
from PIL import Image
from PIL.ExifTags import TAGS

def get_date(filename):
    """ Retrieves the date the photo was taken """
    image = Image.open(filename)
    info = image._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'DateTimeOriginal':
                asciival=str(value).encode('ascii')
                asciistring=asciival.decode('ascii')
                return (asciistring[0:4] + asciistring[5:7] + asciistring[8:10])
    except:
        return 'error'

def rename_files(prefix):
    """ Iterates through the list of files in the current directory.
        For all image files, attempts to rename the file by replacing the prefix
        with the date """
    current_path = os.getcwd()
    file_list = os.listdir(current_path)
    for filename in file_list:
        mimetype = mimetypes.guess_type(filename)[0]
        if mimetype and mimetype.split('/')[0] == "image" and filename.startswith(prefix):
            date_string = get_date(filename)
            if date_string != 'error' and date_string is not None:
                os.rename(filename, date_string + filename[len(prefix):])

def get_prefix():
    """ Parse the prefix to be changed """
    parser = argparse.ArgumentParser(description='A simple file renaming application for easy photo organisation')
    parser.add_argument('prefix', action='store', help='File prefix to search for')

    try:
        options = parser.parse_args()
    except:
        sys.exit(2)

    return options.prefix

if __name__ == "__main__":
    rename_files(get_prefix())
