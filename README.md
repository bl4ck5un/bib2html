Pubs2HTML
=========

Generate publication web pages from BibTeX files.

This is a major rewrite of the backend of Pubs2HTML. It now uses [bibtexparser](https://pypi.python.org/pypi/bibtexparser) to parse the `.bib` and [Jinja2](http://jinja.pocoo.org/) for the reference styling and the output page template.

```
./pubs2html.py -s styles/ieee -t example/template.html example/pubs.bib
```


Usage
-----

```
./pubs2html.py [-h] [-s STYLE] [-t TEMPLATE] [-o OUTPUT] files [files ...]

-h
Display help

-s, --style STYLE
Path to BibTeX style folder. Default: ./styles/default/

-t, --template TEMPLATE
Path to Jinja template file. Default: ./template.html

-o, --output OUTPUT
Output file (if the file already exists, it will be overwritten). Default: ./pubs.html

files
Path to BibTeX file(s) to convert
```

The script aggregates all BibTeX files into a single database which it uses to create the page. It will skip any .bib files that it cannot find or parse.



### BibTeX files

Bibtexparser mimics very well the parsing behavior of BibTeX and you should have no problem using any of your `.bib` files directly. Anything like the following should work perfectly:

	@ENTRY{
		tag1 = "",
		tag2 = "",
		tag3 = ""
	}

Naturally, the better the formatting of your files (especially the content of each tag), the more likely Pubs2HTML will output a nice looking page out of them.



### Styles

A Pubs2HTML style is a folder containing HTML Jinja templates for each supported entry type. The templates define the format of the HTML list items `<li></li>` that will be populated with information from the `.bib` files. Style filenames should be of the form `entrytype.html`. When the Pubs2HTML finds an entry type for which a style has not been defined, it silently ignores it.

Pubs2HTML also looks for a `bib.css` file and makes it available to the output page template through the `css` variable.


#### Custom Jinja filters

Pubs2HTML provides a few Jinja filters to make styling references a little easier.

* `ordinal`: transforms a cardinal input into an ordinal number (useful for edition numbering);
```
<span ...>{{ edition|ordinal }} ed.</span>
```

* `author_join`: like join but for list of words (convenient authors list). It allows you to specify a common separator (default: `,`), a special separator for the last case (default: `, and`), and a special separator for the two value case (default: `and`);
```
<span ...>{{ author|author_join }}</span>
<span ...>{{ author|author_join(', ', ' and ') }}</span>
```




#### The IEEE-like style
Pubs2HTML ships with an "IEEE-like" style definition located in `styles/ieee`. It makes no attempt at being accurate with relation to `IEEEtrans.bst`, but it should have its familiar look. The following entry types are supported:

1. InProceedings
2. Article
3. Book
4. TechReport

The `ieee` style uses patterns loosely inspired on OOCSS (Object Oriented CSS), i.e., the edition tag of a book entry uses ```class="book edition"``` and the title tag of an article entry uses ```class="article title"```. If the style you are attempting to reproduce is similar to that of the IEEE, you may not need to learn Jinja at all: you could get away with just editing `bib.css`.




### HTML template

The output page template is also written using the Jinja templating language. The template design documentation can be found [here](http://jinja.pocoo.org/docs/dev/templates/). Pubs2HTML gives you access to two variables:

* `db`: entries parsed from the BibTeX files. The template has access to both the individual tags (`title`, `author`, `ENTRYTYPE`) and to the formatted ouput of the style (`formatted`).

* `css`: content of `css.bib` file (or an empty string if the file does not exist).

The example template `example/plain.html` provides typical functionalities and can be used as a reference. In general, you should be able turn the HTML of your current publication page into a template with only a few lines of code.



#### Custom Jinja filters

Since you may not want to bundle all your publications together, Pubs2HTML provides the following Jinja filter:

* `keeponly`: filters entries by field. Field values are converted to strings automatically. The default field is the entry type (i.e., `ENTRYTYPE`);
```
<ul id="pubs_list">
	{% for entry in db|keeponly('article') %}
		{{ entry.formatted }}
	{%- endfor %}
</ul>
<ul id="pubs_list">
	{% for entry in db|keeponly(2014, field='year') %}
		{{ entry.formatted }}
	{%- endfor %}
</ul>
```

The same effect could be obtained by using the built in Jinja filter `selectattr(field, 'equalto', value)`. However, the `equalto` test will only be part of Jinja 2.8, so for now this should work.



Issues
------

Issues/suggestions should be report via the GitHub repository:

https://github.com/lchamon/pubs2html
