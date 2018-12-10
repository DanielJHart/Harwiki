import os
import Constant
import Structs

# Global Variables

header = "<!DOCTYPE html>\n<html>\n<head>\n"
footer = "\n</html>"
wikiName = ""
handlingTable = False
listOfPages = list()

# 

# Functions

def IsTableItem(x: str):
	return x == Constant.TABLEIMAGE or x == Constant.TABLEROW or x == Constant.TABLESUBHEADING or x == Constant.TABLEHEADING
# ~IsTableItem

def SetTagsAndReplace(begTag: str, endTag: str, line: str, replace: str, repWith: str):
	line = line.replace(replace + " ", repWith, 1)  
	global handlingTable

	if handlingTable and not IsTableItem(replace):
		begTag = "\n</tbody>\n</table>" + begTag
		handlingTable = False
	
	return begTag, endTag, line
# ~SetTagsAndReplace

def HandleTableRow(line: str):
	begTag, endTag, line = SetTagsAndReplace("\n<tr>", "</tr>", line, Constant.TABLEROW, "\n")
	dashIndex = line.find("-")
	content = ""
	content += "<td style=\"width: 50%\">" + line[:dashIndex] + "</td><td>" + line[dashIndex + 2: -1] + "</td>"
	return begTag, endTag, content

def HandleTableImage(line: str):
	begTag, endTag, line = SetTagsAndReplace("\n<tr>", "</tr>", line, Constant.TABLEIMAGE, "\n")
	content = ""
	content += "<td colspan=\"2\"><img style=\"width: 100%\" src=\"" + line + "\"></td>"
	return begTag, endTag, content

def HandleTableSubheading(line: str):
	begTag, endTag, line = SetTagsAndReplace("\n<tr>", "</tr>", line, Constant.TABLESUBHEADING, "\n")
	content = ""
	content += "<td colspan=\"2\" style=\"width: 100%; font-style: italic; text-align: center; font-weight: 500;\">" + line + "</td>"
	return begTag, endTag, content

def HandleTableHeading(line: str):
	begTag, endTag, line = SetTagsAndReplace("\n<tr><th colspan=\"2\" style=\"text-align: center; font-weight: bold; width: 100%;\">", "</th></tr>", line, Constant.TABLEHEADING, "\n")
	return begTag, endTag, line
	
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
		begTag, endTag, line = SetTagsAndReplace("\n<h1\">", "</h1>", line, Constant.HEADER1, "")
		isHeader = True
	elif line.startswith(Constant.TABLE):
		begTag, endTag, line = SetTagsAndReplace("\n<table class=\"infobox data\" style=\"width:22em\">\n<tbody>", "", line, Constant.TABLE, "")
		handlingTable = True
	elif line.startswith(Constant.TABLEROW):
		begTag, endTag, line = HandleTableRow(line)
	elif line.startswith(Constant.TABLEHEADING):
		begTag, endTag, line = HandleTableHeading(line)
	elif line.startswith(Constant.TABLESUBHEADING):
		begTag, endTag, line = HandleTableSubheading(line)
	elif line.startswith(Constant.TABLEIMAGE):
		begTag, endTag, line = HandleTableImage(line)
	elif line.startswith(Constant.COMMENT):
		begTag, endTag, line = "", "", ""
	else:
		begTag, endTag, line = SetTagsAndReplace("\n<p>", "</p>", line, "", "\n")

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

def CreateSideBar():
	output = ""
	output += "<div id=\"mw-navigation\"><div id=\"mw-panel\">"
	# Here is the side bar
	output += "<div class=\"portal\" role=\"navigation\" id=\"p-interaction\" aria-labelledby=\"p-interaction-label\">"
	output += "<h3 id=\"p-interaction-label\">Pages</h3>"
	output += "<div class=\"body\">"
	output += "<ul>"

	listOfPages.sort()

	for p in listOfPages:
		correctedName = p[p.rfind("/") + 1 : -5]
		correctedText = p
		correctedText = correctedText.replace(wikiName + "/", "")
		correctedText = correctedText[:-5]
		correctedText = correctedText.replace(" ", "%20")
		correctedText = correctedText + ".html"
		htmlLinkText = correctedText
		output += "<li>" + "<a href=\"" + htmlLinkText + "\" title=\"" + correctedName + "\">" + correctedName + "</a></li>"

	output += "</div></div>\n</body>"
	return output

def CreatePage(name: str):
	global wikiName
	file = open(name, "r")
	name = name.replace(".wiki", "")
	print("Creating page: " + name)
	slashPos = name.rfind("/")

	fileContent = file.readlines()

	styleSheetLocation = ""
	styleSheetLocation += os.getcwd().replace("\\", "/")
	styleSheetLocation += "/" + wikiName + "/CSS/"

	construct = header
	construct += "<link rel=\"stylesheet\" type=\"text/css\" href=\"" + styleSheetLocation + "site.css\">\n<link rel=\"stylesheet\" type=\"text/css\" href=\"" + styleSheetLocation + "style.css\">"
	construct += "\n<title>" + name + "</title>\n</head>"
	construct += "\n<body>\n<div id=\"content\" class=\"mw-body\" role=\"main\">\n"
	construct += "<h1 id=\"firstHeading\" class=\"firstHeading\">" + name[slashPos + 1:] + "</h1>"
	construct += "<div id=\"bodyContent\" class=\"mw-body-content\"><div id=\"mw-content-text\" dir=\"ltr\" class=\"mw-content-ltr\">"

	for c in fileContent:
		construct += FormatLineToHTML(c)
	
	construct += "\n</div>\n</div>\n</div>\n"
	construct += CreateSideBar()
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