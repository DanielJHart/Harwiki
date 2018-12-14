import os
import Constant
import Structs

# Global Variables

header = "<!DOCTYPE html>\n<html>\n<head>\n"
footer = "\n</html>"
wikiName = ""
handlingTable = False
listOfPages = list()
contentsTable = ""
placedContents = False
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

	dashPos = line.find(" - ")

	content = ""
	if dashPos < 0:
		content += "<td colspan=\"2\"><img style=\"width: 100%\" src=\"" + line + "\"></td>"
	else:
		content += "<td colspan=\"2\"><img style=\"width: 100%\" src=\"" + line[:dashPos] + "\"></td></tr><tr><td colspan=\"2\" style=\"font-style: italic; text-align: center; font-weight: 500;\">" + line[dashPos + 3:] + "</td>"
	return begTag, endTag, content

def HandleTableSubheading(line: str):
	begTag, endTag, line = SetTagsAndReplace("\n<tr>", "</tr>", line, Constant.TABLESUBHEADING, "\n")
	content = ""
	content += "<td colspan=\"2\" style=\"width: 100%; font-style: italic; text-align: center; font-weight: 500;\">" + line + "</td>"
	return begTag, endTag, content

def HandleTableHeading(line: str):
	begTag, endTag, line = SetTagsAndReplace("\n<tr><th colspan=\"2\" style=\"text-align: center; font-weight: bold; width: 100%;\">", "</th></tr>", line, Constant.TABLEHEADING, "\n")
	return begTag, endTag, line
	
def HandleInlineCommand(i: int, line: str):
	closingBrace = line.find(Constant.INLINECOMMANDEND, i)
	openingBracket = line.find(Constant.INLINECOMMANDTEXTBEG, closingBrace)
	closingBracket = line.find(Constant.INLINECOMMANDTEXTEND, openingBracket)
	commandText = line[i + 1 : closingBrace]
	htmlLinkText = ""
	content = ""
	
	if commandText == Constant.BOLD:
		content += "<b>" + line[openingBracket + 1 :closingBracket] + "</b>"
		skipTo = closingBracket + 1
	elif commandText == Constant.ITALICS:
		content += "<i>" + line[openingBracket + 1 :closingBracket] + "</i>"
		skipTo = closingBracket + 1
	elif commandText == Constant.UNDERLINE:
		content += "<u>" + line[openingBracket + 1 :closingBracket] + "</u>"
		skipTo = closingBracket + 1
	else:
		if commandText.startswith("https"):
			htmlLinkText = commandText
		else:
			fullPath = ""
			for page in listOfPages:
				if page.find(commandText) > - 1:
					fullPath = page[:-5]
				
			if fullPath == "":
				print("Could not find link or command: " + commandText)
				return "", -1
				
			correctedText = fullPath
			correctedText = correctedText.replace(wikiName + "/", "")
			correctedText = correctedText.replace(" ", "%20")
			correctedText = correctedText + ".html"
			htmlLinkText = correctedText

		content = "<a href =\"" + htmlLinkText + "\">" + line[openingBracket + 1 :closingBracket] + "</a>"
		skipTo = closingBracket + 1
	return content, skipTo

def FormatLine(line: str):
	content = ""
	skipTo = 0
	for i in range(len(line)):
		if i < skipTo:
			continue
		
		c = line[i]
		if c == Constant.INLINECOMMANDBEG:
			ret, skipTo = HandleInlineCommand(i, line)
			content += ret
		else:
			content += c

	return content

def FormatLineToHTML(line: str):
	begTag = ""
	endTag = ""
	content = ""
	isHeader = False
	
	global handlingTable
	global placedContents

	if line.startswith(Constant.HEADER3):
		begTag, endTag, line = SetTagsAndReplace("\n<h3>", "</h3>", line, Constant.HEADER3, "")
		isHeader = True
	elif line.startswith(Constant.HEADER2):
		begTag, endTag, line = SetTagsAndReplace("\n<h2>", "</h2>", line, Constant.HEADER2, "")
		
		if not placedContents:
			begTag = contentsTable + begTag
			placedContents = True

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

	content = FormatLine(line)

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

def CreateTableOfContents(lines):
	content = "<div id=\"toc\" class=\"toc\"><div class=\"toctile\" lang=\"en\" dir=\"ltr\"><h2>Contents</h2>\n</div><ul>"
	subheadingNumber = 1
	inSubHeading = False
	section = 1
	heading = 0
	
	for line in lines:
		if line.startswith(Constant.HEADER3):
			cleanedText = line.replace(Constant.HEADER3 + "", "")
			content += "<li class=\"toclevel-2 tocsection-" + str(section) + "\"><a href=\"#" + cleanedText + "\"><span class=\"tocnumber\">" + str(heading) + "." + str(subheadingNumber) + "</span><span class=\"toctext\">" + cleanedText + "</span></a></li>"
			subheadingNumber += 1
			inSubHeading = True
			section += 1
		elif line.startswith(Constant.HEADER2):
			cleanedText = line.replace(Constant.HEADER2 + "", "")
			heading += 1
			if inSubHeading:
				content += "</ul></li>"
				subheadingNumber = 1
				inSubHeading = False
			
			content += "<li class=\"toclevel-1 tocsection-" + str(section) + "\"><a href=\"#" + cleanedText + "\">" + str(heading) + cleanedText + "<ul>"

			isHeader = True
			
			section += 1
	
	content += "</ul></a></li></ul></div>"
	return content

def CreatePage(name: str):
	global wikiName
	global contentsTable
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
	
	contentsTable = CreateTableOfContents(fileContent)
	
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