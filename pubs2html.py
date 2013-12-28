#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, time, argparse
import outputhtml, bibparser

PATH = os.getcwdu()


# Create command line arguments parser
parser = argparse.ArgumentParser()

# Command line arguments
parser.add_argument('-t', '--template', default = os.path.join( PATH, 'template.html' ), help = 'Path of template file. Default: ./template.html')
parser.add_argument('-o', '--output', default = os.path.join( PATH, 'pubs.html' ), help = 'Path of output file (if the file already exists, it will be overwritten). Default: ./pubs.html')
parser.add_argument('files', nargs = '+', help = 'Path to BibTeX file(s) to convert')

# Parse command line arguments
args = parser.parse_args()


# Check template file exists
if os.path.isfile(args.template):
	# Start conversion
	# Create empty database
	db = []

	# for filePath in FILE_LIST:
	for filePath in args.files:
		# Read BibTeX file
		try:
			inputFile = open( filePath, 'r' )
			bibtex = inputFile.read()
			inputFile.close()

			# Separate each BibTeX entry in the file
			bibparser.parse( bibtex, db )
		except IOError:
			print 'An error occured while processing the file "' + filePath + '". Its content will be ignored.'


	# Sort entries by year (primary key, reverse) then author (secondary key)
	db.sort(key = lambda entry: entry['author'])
	db.sort(key = lambda entry: entry['year'], reverse = True)

	try:
		# Create output and template file
		outputFile = open( args.output, 'w' )
		templateFile = open( args.template, 'r' )

		# Generate HTML file
		outputhtml.gen( db, templateFile, outputFile )

		# Close files
		templateFile.close()
		outputFile.close()
	except IOError:
		print 'An error occured while processing the template and output files. The program will exit without completing the task.'
else:
	print 'Template file was not found at "' + args.template + '".'