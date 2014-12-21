#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
from copy import deepcopy

import bibtexparser
from bibtexparser.bparser import BibTexParser
from jinja2 import Environment, FileSystemLoader

from auxfun import *


PATH = os.getcwdu()

# Create command line arguments parser
parser = argparse.ArgumentParser()

# Command line arguments
parser.add_argument('-t', '--template',
                    default=os.path.join(PATH, 'template.html'),
                    help='Path of templates folder. Default: ./template.html')
parser.add_argument('-s', '--style',
                    default=os.path.join(PATH, 'styles/default'),
                    help='Path to style folder. Default: ./styles/default/')
parser.add_argument('-o', '--output',
                    default=os.path.join(PATH, 'pubs.html'),
                    help='Output file (if the file already exists, '
                         'it will be overwritten). Default: ./pubs.html')
parser.add_argument('files', nargs='+', help='Path to BibTeX file(s) to convert',
                    default=os.path.join(PATH, 'pubs.bib'))

# Parse command line arguments
args = parser.parse_args()


if not os.path.isdir(args.style):
    raise Exception('Style argument [' + args.style + '] must be a folder.')

if not os.path.isfile(args.template):
    raise Exception('Template [' + args.template + '] must be a file.')


# Start BibTeX files parsing
# Create empty database
db = []

# Parse each file and merge databases
for filePath in args.files:
    # Read BibTeX file
    try:
        # Add customizations to the BibTeX parser
        parser = BibTexParser()
        parser.customization = customizations

        # Load and parse BibTeX file
        inputFile = open(filePath, 'r')
        dbTemp = bibtexparser.load(inputFile, parser=parser).entries
        inputFile.close()

        # Check if entry title isn't duplicated then add entry to database
        for entryTemp in dbTemp:
            if not any(entryTemp['title'].lower() == entry['title'].lower() for entry in db):
                db.append(deepcopy(entryTemp))

    except IOError:
        print ('An error occured while processing [' +
               filePath + ']. Its content will be ignored.')


# Format entries according to selected style and write to file
try:
    # Setup Jinja environment for BibTeX entries styling
    bibEnv = Environment(loader=FileSystemLoader(args.style))
    supportedStyles = [os.path.splitext(file)[0] for file in bibEnv.list_templates('html')]
    bibEnv.filters['ordinal'] = ordinal
    bibEnv.filters['author_join'] = author_join

    for entry in db:
        if entry['ENTRYTYPE'] in supportedStyles:
            bibTemplate = bibEnv.get_template(entry['ENTRYTYPE'] + '.html')
            entry['formatted'] = bibTemplate.render(entry)

    # Read in css file or leave blank if it does not exist
    cssPath = os.path.join(args.style, 'bib.css')
    if os.path.isfile(cssPath):
        cssFile = open(cssPath, 'r')
        css = cssFile.read()
        cssFile.close()
    else:
        css = ''

except:
    print ('An error occured while processing the style files.'
           'The program will exit without completing the task.')

else:
    try:
        # Setup Jinja environment for output template
        outputEnv = Environment(loader=FileSystemLoader(os.path.dirname(args.template)))
        outputEnv.filters['keeponly'] = keeponly
        outputTemplate = outputEnv.get_template(os.path.basename(args.template))

        # Write to output file
        outputFile = open(args.output, 'w')
        outputFile.write(outputTemplate.render(db=db, css=css).encode('utf8'))
        outputFile.close()

    except IOError:
        print ('An error occured while processing the template file.'
               'The program will exit without completing the task.')
