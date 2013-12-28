#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
from copy import deepcopy

SUPPORTED_ENTRIES = ('book', 'inproceedings', 'article')
REQUIRED_FIELDS =	{
						'book' : ('author', 'title', 'publisher', 'year'),
						'inproceedings' : ('author', 'title', 'booktitle', 'year'),
						'article' : ('author', 'title', 'journal', 'year')
					}


def parse( bibtex, db ):
	# Separate each BibTeX entry in the file
	entries = re.findall( '@(\w+){([^}]+)}', bibtex )

	# For each entry...
	for entry in entries:
		# - check if entry type is supported (otherwise, ignore entry)
		if entry[0].lower() in SUPPORTED_ENTRIES:
			# - save entry type
			entryFields = {'type' : entry[0].lower()}
			
			# - get entry fields
			fields = re.findall('([a-z]+)\s*=\s*\"([^\"]+)\"',entry[1])
			for f in fields:
				entryFields[ f[0].lower() ] = f[1]
				
			# - check if all required fields for entry type are filled (otherwise, ignore entry)
			if all(f in entryFields for f in REQUIRED_FIELDS[ entryFields['type'] ] ):
				# - format the authors field
				authorList = re.split( 'and|\&', entryFields['author'])
				authorList = [x.strip() for x in authorList]
				if len(authorList) == 2:
					entryFields['author'] = ' and '.join(authorList)
				elif len(authorList) > 2:
					entryFields['author'] = ', '.join(authorList[0:-1]) + ', and ' + authorList[-1]
				
				# - append to database if no title matches the title of the current entry
				if not any( entryDB['title'].lower() == entryFields['title'].lower() for entryDB in db ):
					db.append( deepcopy(entryFields) )
			else:
				print '[Missing fields] Entry is missing required fields "' + entry[0].strip() + ' -- ' + entry[1].strip() + '"\n\n'
		else:
			print '[Unsupported type] Entry has unsupported type "' + entry[0].strip() + ' -- ' + entry[1].strip() + '"\n\n'
		
	
	return db

