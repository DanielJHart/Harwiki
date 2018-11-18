import os
import Constant
import Structs

# Global Variables

header = "<!DOCTYPE html>\n<html>\n"
footer = "\n</html>"
wikiName = ""
handlingTable = False
# 

# Functions
def IsTableItem(x: str):
    return x == Constant.TABLEIMAGE or x == Constant.TABLEROW

def SetTagsAndReplace(begTag: str, endTag: str, line: str, replace: str, repWith: str):
    line = line.replace(replace + " ", repWith, 1)  
    global handlingTable

    if handlingTable and IsTableItem(replace):
        endTag += "\n</tbody>\n</table>"
        handlingTable = False
    
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
        begTag, endTag, line = SetTagsAndReplace("\n<h1>", "</h1>", line, Constant.HEADER1, "")
        isHeader = True
    elif line.startswith(Constant.PARAGRAPH):
        begTag, endTag, line = SetTagsAndReplace("\n<p>", "</p>", line, Constant.PARAGRAPH, "\n")
    elif line.startswith(Constant.TABLE):
        begTag, endTag, line = SetTagsAndReplace("\n<table>\n<tbody>", "", line, Constant.TABLE, "\n")
        handlingTable = True
    elif line.startswith(Constant.TABLEROW):
        begTag, endTag, line = SetTagsAndReplace("\n<tr>", "</tr>", line, Constant.TABLEROW, "\n")
        

#    i = -1
#    i = line.find(Constant.LINK)
#    if i >= 0:
#        endOfLink = line.index("]", i) # Gets the length of the link
#        startOfText = line.index("(", endOfLink)
#        endOfText = line.index(")", endOfLink)
        
        

    if isHeader:
        line = line[:-1]

    content += line

    return begTag + content + endTag
    

def CreatePage(name: str):
    file = open(wikiName + "/" + name, "r")
    name = name.replace(".txt", "")
    print("Creating page: " + name)

    fileContent = file.readlines()

    construct = header
    construct += "<head>\n<title>" + name + "</title>\n</head>"
    construct += "\n<body>"
   
    for c in fileContent:
        construct += FormatLineToHTML(c)
    
    construct += "\n</body>"
    construct += footer

    out = open(wikiName + "/" + name + ".html", "w")
    out.write(construct)
    out.close()
    
# Main

wikiName = input("Enter the name of your wiki: ")

#fullContent = "<!DOCTYPE html>\n<html>\n<head>\n<title>" + wikiName + "</title>\n</head>\n<body>\n\n<h1>This is a Heading</h1>\n<p>This is a paragraph.</p>\n\n</body>\n</html>"

dir = os.listdir(wikiName)
print(dir)

for f in dir:
    if f.endswith(".txt"):
        CreatePage(f)

# ~Main