# Harwiki
A tool to generate a wiki from a set of text files

## How it works
* Harwiki will ask you for a directory where your files are stored.
* It will go through the files and create an HTML page for each
* It will link these pages and add images as necessary

## The Text Files
The text files will have to be a in a specific format. The commands and how to use them are listed below:

## Commands
A command is designated with -*- at the start of a paragraph where * is the command to be done.

### Headers
A header is set with -H*- where * is the header number. 
For example "-H1- This is the top header" would generate:
# This is the top header

### Paragraphs
A paragraph is set with a -P- at the front. This generates a normal paragraph.

### Tables
Tables are started with a -T- and each table item is started with a -Tr-. Once an element is found that is not a table row, the table is closed.

## Inline Commands
Inline commands are used for things like making text bold, italic or linking to something else.

### Links
Links are styled as [link](text). The link can either be to a webpage, or (in the future) will take a file name and link to that file.
