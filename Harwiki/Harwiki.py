import os
import Constant
import structs

# Global Variables

header = "<!DOCTYPE html>\n<html>\n"
footer = "\n</html>"
wikiName = ""


# Functions
def FormatLineToHTML(line: str):
    begTag = ""
    endTag = ""
    content = ""
    isHeader = False

    if line.endswith("\n"):
        line = line[:-1]

    if line.startswith(Constant.HEADER3):
        begTag = "\n<h3>"
        endTag = "</h3>"
        line = line.replace(Constant.HEADER3 + " ", "", 1)
        isHeader = True
    elif line.startswith(Constant.HEADER2):
        begTag = "\n<h2>"
        endTag = "</h2>"
        line = line.replace(Constant.HEADER2 + " ", "", 1)
        isHeader = True
    elif line.startswith(Constant.HEADER1):
        begTag = "\n<h1>"
        endTag = "</h1>"
        line = line.replace(Constant.HEADER1 + " ", "", 1)
        isHeader = True

    if not isHeader:
        content += "\n"

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