import os
import Constant
import Structs

# Global Variables

header = "<!DOCTYPE html>\n<html>\n"
footer = "\n</html>"
wikiName = ""
handlingTable = False
listOfPages = list()

# 

# Functions

def IsTableItem(x: str):
	return x == Constant.TABLEIMAGE or x == Constant.TABLEROW
# ~IsTableItem

def SetTagsAndReplace(begTag: str, endTag: str, line: str, replace: str, repWith: str):
	line = line.replace(replace + " ", repWith, 1)  
	global handlingTable

	if handlingTable and IsTableItem(replace):
		endTag += "\n</tbody>\n</table>"
		handlingTable = False
	
	return begTag, endTag, line
# ~SetTagsAndReplace

def FormatLineToHTML(line: str):
	begTag = ""
	endTag = ""
	content = ""
	isHeader = False
	global handlingTable

	if line.startswith(Constant.HEADER3):
		begTag, endTag, line = SetTagsAndReplace("\n<h3>", "</h3>", line, Constant.HEADER3, "")
		isHeader = True
	elif line.startswith(Constant.HEADER2):
		begTag, endTag, line = SetTagsAndReplace("\n<h2>", "</h2>", line, Constant.HEADER2, "")
		isHeader = True
	elif line.startswith(Constant.HEADER1):
		begTag, endTag, line = SetTagsAndReplace("\n<h1 id=\"firstHeading\" class=\"firstHeading\">", "</h1>", line, Constant.HEADER1, "")
		isHeader = True
	elif line.startswith(Constant.PARAGRAPH):
		begTag, endTag, line = SetTagsAndReplace("\n<p>", "</p>", line, Constant.PARAGRAPH, "\n")
	elif line.startswith(Constant.TABLE):
		begTag, endTag, line = SetTagsAndReplace("\n<table>\n<tbody>", "", line, Constant.TABLE, "")
		handlingTable = True
	elif line.startswith(Constant.TABLEROW):
		begTag, endTag, line = SetTagsAndReplace("\n<tr>", "</tr>", line, Constant.TABLEROW, "\n")
		
	if isHeader:
		line = line[:-1]

	content = ""
	skipTo = 0
	for i in range(len(line)):
		if i < skipTo:
			continue
		
		c = line[i]
		if c == Constant.LINKBEG:
			closingBrace = line.find(Constant.LINKEND, i)
			openingBracket = line.find(Constant.LINKTBEG, closingBrace)
			closingBracket = line.find(Constant.LINKTEND, openingBracket)
			linkText = line[i + 1 : closingBrace]
			htmlLinkText = ""
			
			if linkText.startswith("https"):
				htmlLinkText = linkText
			else:
				fullPath = ""
				for page in listOfPages:
					if page.find(linkText) > - 1:
						fullPath = page[:-5]
				
				if fullPath == "":
					print("Could not find link: " + linkText)
					continue
				
				correctedText = fullPath
				correctedText = correctedText.replace(wikiName + "/", "")
				correctedText = correctedText.replace(" ", "%20")
				correctedText = correctedText + ".html"
				htmlLinkText = correctedText

			content += "<a href =\"" + htmlLinkText + "\">" + line[openingBracket + 1 :closingBracket] + "</a>"
			skipTo = closingBracket + 1
		else:
			content += c

	return begTag + content + endTag
# ~FormatLineToHTML

def CreatePage(name: str):
	global wikiName
	file = open(name, "r")
	name = name.replace(".wiki", "")
	print("Creating page: " + name)

	fileContent = file.readlines()

	construct = header
	construct += "<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"shared.css\">\n<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">\n<title>" + name + "</title>\n</head>"
	construct += "\n<body>\n<div id=\"content\" class=\"mw-body\" role=\"main\">\n<div id=\"bodyContent\" class=\"mw-body-content\">"

	for c in fileContent:
		construct += FormatLineToHTML(c)
	
	construct += "\n</div>\n</div>\n<div id=\"mw-navigation\"><div id=\"mw-panel\"></div></div>\n</body>"
	construct += footer

	out = open(name + ".html", "w")
	out.write(construct)
	out.close()
# ~CreatePage

def IsFolder(name: str):
	return name.find(".") == -1

def GatherWikiFiles(dir, currentDir: str):
	global listOfPages
	for f in dir:
		if f.endswith(".wiki"):
			print ("adding " + currentDir + "/" + f)
			listOfPages.append(currentDir + "/" + f)
		elif IsFolder(f):
			folderPath = currentDir + "/" + f
			GatherWikiFiles(os.listdir(folderPath), folderPath)

def Main():
	global wikiName, listOfPages
	wikiName = input("Enter the name of your wiki: ")

	dir = os.listdir(wikiName)

	# Get all of the 
	GatherWikiFiles(dir, wikiName)

	for page in listOfPages:
		CreatePage(page)
	

# ~Main

Main()