Pubs2HTML
=========

These scripts will generate a publication web pages based on BibTeX files and a custom template. It outputs an HTML list markup with CSS classes that allows different styling of the elements. The publications are ordered in reverse chronological order and then in alphabetical order of first author name.



Usage
-----

```
./pubs2html.py [-h] [-t TEMPLATE] [-o OUTPUT] files [files ...]

-h
Display help

-t, --template TEMPLATE
Path of template file. Default: ./template.html

-o, --output OUTPUT
Path of output file (if the file already exists, it will be overwritten). Default: ./pubs.html

files
Path to BibTeX file(s) to convert
```

The script will output errors to stdout specifying the error and the entry where it occurred. It will, however, skip the problematic file and keep processing the provided BibTeX databases. Hence, it will generate a web page with as many entries as it could parse.

You can run this script in a cron to automatically update your publications page every week or month. The advantage of this method is that you deliver a static page to users (which is faster), even though it is automatically updated from time to time.



### BibTeX format

This script uses a fairly simple BibTeX parser, so it does have a few limitations. Some more advanced BibTeX tags that are unnecessary for a common publication web page are not supported and will simply be ignored. For the script to work, your .bib file must follow these rules:

- Entries must be enclosed in braces ```{}``` (even though BibTeX supports other characters)
- Tag values must be enclosed in double quotes ```""``` (again this is despite BibTeX's support for other characters)
- Each tag should be on its own line

Here's a template of what an entry should look like:
```
@ENTRY{
tag1 = "",
tag2 = "",
tag3 = ""
}
```


#### Supported entry types
1. InProceedings
2. Article
3. Book


#### Additional PDF URL tag
You can provide an URL to your paper using the special tag ```pdfurl```, e.g.,

```
pdfurl = "http://www.lps.usp.br/chamon/pdf/chamon_eusipco2013.pdf"
```

It will then show up as a link in the markup. If absent, the link is not displayed.



### HTML template

The script will replace any occurrence of the placeholders in the file with the generated markup. Hence, by providing a valid HTML file you can automatically generate your publication web page. The supported placeholders are

	- @@INPROCEEDINGS@@
	- @@ARTICLE@@
	- @@BOOK@@

**Note**: Placeholders should be placed on an _empty line_.



### CSS styling

The CSS classes used to style the items loosely follow an OOCSS (Object Oriented CSS) pattern, i.e., the edition tag of a book entry uses ```class="book edition"``` and the title tag of an article entry uses ```class="article title"```. The default styling provided in example/css/bib.css mimics the IEEE reference style and contains all the CSS classes used in the current version.