#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

PATH = os.getcwdu()



# Complete HTML ################################
def gen( db, templateFile, outputFile ):
	# Copy template file, replacing placeholders by the respective database entries
	for line in templateFile:
		# Output the all entries in the database
		if line.strip() == '@@ALL@@':
			for entry in db:
				outputFile.write( globals()[entry['type']](entry) )
		
		# Output only entries of type INPROCEEDINGS
		elif line.strip() == '@@INPROCEEDINGS@@':
			for entry in [ e for e in db if e['type'] == 'inproceedings' ]:
				outputFile.write( inproceedings(entry) )
		
		# Output only entries of type ARTICLE
		elif line.strip() == '@@ARTICLE@@':
			for entry in [ e for e in db if e['type'] == 'article' ]:
				outputFile.write( article(entry) )
		
		# Output only entries of type BOOK
		elif line.strip() == '@@BOOK@@':
			for entry in [ e for e in db if e['type'] == 'book' ]:
				outputFile.write( book(entry) )

		# Otherwise, just output the template file content
		else:
			outputFile.write(line)
# ##############################################


# Book format ##################################
def book( entry ):
	entryType = 'book'
	
	# Open list item tag
	htmlStr = ('<li>\n')
	
	htmlStr = htmlStr + '<span class="' + entryType + ' author">' + entry['author'] + '</span>,\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' title">' + entry['title'] + '</span>.\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' publisher">' + entry['publisher'] + '</span>, '
	
	if 'edition' in entry:
		htmlStr = htmlStr + '<span class="' + entryType + ' edition">'
		if entry['edition'] > 3:
			htmlStr = htmlStr + entry['edition'] + 'th'
		elif entry['edition'] == 2:
			htmlStr = htmlStr + '2nd'
		elif entry['edition'] == 3:
			htmlStr = htmlStr + '3rd'
		elif entry['edition'] == 1:
			htmlStr = htmlStr + '1st'
		htmlStr = htmlStr + ' edition</span>, '
	
	htmlStr = htmlStr + '<span class="' + entryType + ' year">' + entry['year'] + '</span>.\n'
	
	# File link
	if 'pdfurl' in entry:
		htmlStr = htmlStr + '[<a href="' + entry['pdfurl'] + '">pdf</a>].\n'
	
	# Close list item tag
	htmlStr = htmlStr +'</li>\n'
	
	return htmlStr
# ##############################################


# Conference format ############################
def inproceedings( entry ):
	entryType = 'conference'
	
	# Open list item tag
	htmlStr = '<li>\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' author">' + entry['author'] + '</span>,\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' title">' + entry['title'] + '</span>.\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' booktitle">' + entry['booktitle'] + '</span>, '
	
	if 'address' in entry:
		htmlStr = htmlStr + '\n<span class="' + entryType + ' address">' + entry['address'] + '</span>,\n'
		
	if 'pages' in entry:
		htmlStr = htmlStr + '<span class="' + entryType + ' pages"> pp. ' + entry['pages'] + '</span>, '
	
	htmlStr = htmlStr + '<span class="' + entryType + ' year">' + entry['year'] + '</span>.\n'
	
	# File link
	if 'pdfurl' in entry:
		htmlStr = htmlStr + '[<a href="' + entry['pdfurl'] + '">pdf</a>].\n'
	
	# Close list item tag
	htmlStr = htmlStr +'</li>\n'
	
	return htmlStr
# ##############################################


# Journal format ############################
def article( entry ):
	entryType = 'article'
	
	# Open list item tag
	htmlStr = '<li>\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' author">' + entry['author'] + '</span>,\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' title">' + entry['title'] + '</span>.\n'
	
	htmlStr = htmlStr + '<span class="' + entryType + ' journal">' + entry['journal'] + '</span>, '
	
	if 'volume' in entry:
		htmlStr = htmlStr + '<span class="' + entryType + ' volume"> vol. ' + entry['volume'] + '</span>, '
	
	if 'pages' in entry:
		htmlStr = htmlStr + '<span class="' + entryType + ' pages"> pp. ' + entry['pages'] + '</span>, '
	
	htmlStr = htmlStr + '<span class="' + entryType + ' year">' + entry['year'] + '</span>.\n'
	
	# File link
	if 'pdfurl' in entry:
		htmlStr = htmlStr + '[<a href="' + entry['pdfurl'] + '">pdf</a>].\n'
	
	# Close list item tag
	htmlStr = htmlStr +'</li>\n'
	
	return htmlStr
# ##############################################
