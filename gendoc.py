# WARNING: This file is a mess

from os import listdir, path, mkdir
from os.path import isfile, join
import json
import re
import shutil
import html as htmlModule

SPECS_FOLDER = "specs"
TEMPLATES_FOLDER = "templates"
OUTPUT_FOLDER = "dist"

searchIndex = []

specTemplate = ""
opcodeTemplate = ""
infoTemplate = ""
registersTemplate = ""
glossaryTemplate = ""

indexTemplate = ""
searchCardTemplate = ""

def seofyname(name):
    return '-'.join(list(filter(None, name.lower().replace(".", "-").replace("(", "-").replace(")", "-").replace(" ", "-").split("-"))))

# Loads all needed templates
with open(TEMPLATES_FOLDER + "/spec.html.template", "r") as f:
    specTemplate = f.read()

with open(TEMPLATES_FOLDER + "/opcode.html.template", "r") as f:
    opcodeTemplate = f.read()

with open(TEMPLATES_FOLDER + "/info.html.template", "r") as f:
    infoTemplate = f.read()

with open(TEMPLATES_FOLDER + "/registers.html.template", "r") as f:
    registersTemplate = f.read()

with open(TEMPLATES_FOLDER + "/glossary.html.template", "r") as f:
    glossaryTemplate = f.read()

with open(TEMPLATES_FOLDER + "/index.html.template", "r") as f:
    indexTemplate = f.read()

with open(TEMPLATES_FOLDER + "/search-card.html.template", "r") as f:
    searchCardTemplate = f.read()

# Obtains all spec files.
specFiles = sorted([SPECS_FOLDER + "/" + f for f in listdir(SPECS_FOLDER) if isfile(join(SPECS_FOLDER, f))])

# Creates the output folder
if not path.exists(OUTPUT_FOLDER):
    mkdir(OUTPUT_FOLDER)

with open(OUTPUT_FOLDER + "/index.html", "w") as indexHTMLFile:
    indexFileLines = indexTemplate.split("\n")
    for ifl in indexFileLines:
        m = re.search("{{(.*?)}}", ifl)
        if m and (m[1] == "content"):
            for f in specFiles:
                with open(f, "r") as spec:
                    specsJson = json.load(spec)

                # Write search card
                searchCardLines = searchCardTemplate.split("\n")
                for scl in searchCardLines:
                    m = re.search("{{(.*?)}}", scl)
                    if m:
                        if m[1] == "link":
                            scl = scl.replace("{{" + m[1] + "}}", specsJson["$info"]["title"] + ".html")
                        else:
                            scl = scl.replace("{{" + m[1] + "}}", specsJson["$info"][m[1]])

                    indexHTMLFile.write(scl)

                with open(OUTPUT_FOLDER + "/" + specsJson["$info"]["title"] + ".html", "w") as html:
                    lines = specTemplate.split("\n")
                    for l in lines:
                        m = re.search("{{(.*?)}}", l)
                        if m:
                            if m[1] == "content":

                                if not specsJson["$info"]["complete"]:
                                    html.write("<div class='missing'>Information is missing, please help to complete this page.</div>")

                                # Headertemplate
                                html.write("<h2 id='info'>Specification info</h2>")
                                linesInfo = infoTemplate.split("\n")
                                for li in linesInfo:
                                    ml = list(filter(None, re.findall("{{(.*?)}}", li)))
                                    dontPrint = False
                                    for match in ml:
                                        if match == "sources":
                                            for s in specsJson["$info"]["sources"]:
                                                html.write("<li><a href='" + s + "' target='_blank'>" + s + "</a></li>\n")
                                            dontPrint = True
                                        elif match == "seoname":
                                            li = li.replace("{{" + match + "}}", seofyname(specsJson["$info"]["title"]))
                                        elif match == "spec":
                                            li = li.replace("{{" + match + "}}", f)
                                        elif match == "caches":
                                            for c in specsJson["$info"]["cache"].keys():
                                                html.write("<tr><td>" + c + "</td><td>" + specsJson["$info"]["cache"][c]["size"] + "</td>")
                                                if "comment" in specsJson["$info"]["cache"][c]:
                                                    html.write("<td>" + specsJson["$info"]["cache"][c]["comment"] + "</td>")

                                                html.write("</tr>")

                                            dontPrint = True
                                        else:
                                            if match in specsJson["$info"]:
                                                li = li.replace("{{" + match + "}}", str(specsJson["$info"][match]))
                                            else:
                                                li = li.replace("{{" + match + "}}", "")
                                    
                                    if not dontPrint:
                                        html.write(li + "\n")
                                    else:
                                        dontPrint = False

                                # Glossarytemplate
                                if "glossary" in specsJson:
                                    html.write("<h2 id='info'>Glossary</h2>")
                                    linesInfo = glossaryTemplate.split("\n")
                                    for li in linesInfo:
                                        ml = list(filter(None, re.findall("{{(.*?)}}", li)))
                                        dontPrint = False

                                        for match in ml:
                                            if match == "glossary":
                                                for glossary in specsJson["glossary"]:
                                                    html.write("<tr><td>" + htmlModule.escape(glossary) + "</td><td>" + specsJson["glossary"][glossary] + "</td></tr>")

                                                dontPrint = True

                                        if not dontPrint:
                                            html.write(li + "\n")
                                        else:
                                            dontPrint = False

                                # Registers
                                html.write("<h2 id='registers'>Registers</h2>")

                                for p in specsJson["registers"].keys():
                                    linesInfo = registersTemplate.split("\n")
                                    for li in linesInfo:
                                        ml = list(filter(None, re.findall("{{(.*?)}}", li)))
                                        dontPrint = False
                                        for match in ml:
                                            if match == "registers":
                                                for r in specsJson["registers"][p]:
                                                    html.write("<tr><td style='text-align:left'>" + r["name"] + "</td><td style='text-align:left'>" + r["value"] + "</td><td style='text-align:left'>" + str(r["size"]) + "</td></tr>\n")
                                                dontPrint = True
                                            elif match == "seoname":
                                                li = li.replace("{{" + match + "}}", seofyname(p))
                                            elif match == "processor":
                                                li = li.replace("{{" + match + "}}", p + "-Processor")
                                        
                                        if not dontPrint:
                                            html.write(li + "\n")
                                        else:
                                            dontPrint = False

                                # Opcode template
                                lastGroup = 0
                                for c in specsJson["opcodes"]:
                                    if c["group"] != lastGroup:
                                        lastGroup = c["group"]
                                        html.write("<h2 id='" + seofyname(specsJson["groups"][lastGroup - 1]) + "'>" + specsJson["groups"][lastGroup - 1] + "</h2>\n")

                                    index = []
                                    fields = ["name", "format", "purpose", "description"]

                                    for field in fields:
                                        if field in c:
                                            index.append(c[field])

                                    searchIndex.append({
                                        "href": seofyname(c["name"]),
                                        "index": index
                                    })

                                    linesOp = opcodeTemplate.split("\n")
                                    for lp in linesOp:
                                        ml = list(filter(None, re.findall("{{(.*?)}}", lp)))
                                        dontPrint = False
                                        for match in ml:
                                            if match == "headers":
                                                for k in c["decode"].keys():
                                                    html.write("<th>" + k + "</th>\n")
                                                dontPrint = True
                                            elif match == "bits":
                                                for k in c["decode"].keys():
                                                    html.write("<td>" + str(c["decode"][k]) + "</td>\n")
                                                dontPrint = True
                                            elif match == "seoname":
                                                lp = lp.replace("{{" + match + "}}", seofyname(c["name"]))
                                            # elif match == "format":
                                            #     fmt = c[match]
                                            #     if "glossary" in specsJson:
                                            #         fmtlist = re.split(",|\[|\]| |\(|\)", fmt)
                                            #         fmt = ""

                                            #         for part in fmtlist:
                                            #             if part in specsJson["glossary"]:
                                            #                 fmt += "<span class='glossary' title='" + specsJson["glossary"][part] + "'>" + htmlModule.escape(part) + "</span>"
                                            #             else:
                                            #                 fmt += part

                                            #         print (fmtlist)

                                            #         #for glossary in specsJson["glossary"].keys():
                                            #         #    fmt = fmt.replace(glossary, "<span class='glossary' title='" + specsJson["glossary"][glossary] + "'>" + htmlModule.escape(glossary) + "</span>")

                                            #     lp = lp.replace("{{" + match + "}}", fmt)
                                            else:
                                                if match in c:
                                                    lp = lp.replace("{{" + match + "}}", str(c[match]))
                                                else:
                                                    lp = lp.replace("{{" + match + "}}", "Nothing or missing documentation")
                                        
                                        if not dontPrint:
                                            html.write(lp + "\n")
                                        else:
                                            dontPrint = False
                                continue
                            elif m[1] == "groups":
                                html.write("<li><a href='#info' onclick='hideMenu()'>Specification info</a></li>")

                                if "glossary" in specsJson:
                                    html.write("<li><a href='#glossary' onclick='hideMenu()'>Glossary</a></li>")

                                html.write("<li><a href='#registers' onclick='hideMenu()'>Registers</a></li>")
                                for g in specsJson["groups"]:
                                    html.write("<li><a href='#" + seofyname(g) + "' onclick='hideMenu()'>" + g + "</a></li>")
                                continue
                            elif m[1] == "searchIndex":
                                json.dump(searchIndex, html)
                                continue
                            else:
                                l = l.replace("{{" + m[1] + "}}", specsJson["$info"][m[1]])

                        html.write(l + "\n")
        else:
            indexHTMLFile.write(ifl + "\n")

# Copies all needed files to the output folder
shutil.copy("main.js", OUTPUT_FOLDER + "/main.js")
shutil.copy("search.js", OUTPUT_FOLDER + "/search.js")
shutil.copy("spec.js", OUTPUT_FOLDER + "/spec.js")
shutil.copy("styles.css", OUTPUT_FOLDER + "/styles.css")
shutil.copy("index.css", OUTPUT_FOLDER + "/index.css")
shutil.copy("spec.css", OUTPUT_FOLDER + "/spec.css")

try:
    shutil.copytree("fonts", OUTPUT_FOLDER + "/fonts")
except:
    pass

try:
    shutil.copytree("specs", OUTPUT_FOLDER + "/specs")
except:
    pass