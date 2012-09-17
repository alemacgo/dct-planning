#!/usr/bin/env python
# TODO: Add form validation

#def format_string(s, number_of_chars):
#    lines = s.lines()
#    for line in lines:
#        l = []
#        for i in range(0, len(line), number_of_chars):
#            l.append(s[i:i+number_of_chars])
#        string.append(
#    return '\n'.join(l)

import cgi, cgitb, os
cgitb.enable()

#cgi.test()
print "Content-type: text/html\n\n"
form = cgi.FieldStorage()

formula = form.getvalue('formula')
signature = form.getvalue('signature')

if formula is not None:
    file = open("dct/problem.dct", 'w')
    file.write(formula)
    file.close()
else: formula = ""

if signature is not None:
    file = open("dct/problem.sig", 'w')
    file.write(signature)
    file.close()
else: signature = ""

file = open("dct/problem.ins", 'r')
structure = file.read()
file.close()

if os.system("((bin/soplan.py --nocolor --output=dct/domain.pddl dct/problem.dct) >/dev/null) 2>bin/error.log"):
    domain = ""
    file = open("bin/error.log", "r")
    error = file.read()
    file.close()
else:
    error = ""
    file = open("dct/domain.pddl", "r")
    domain = file.read()
    file.close()

html_page = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>Second-order logic into STRIPS</title>
    <script src="codemirror/js/codemirror.js" type="text/javascript"></script> 
    <link rel="stylesheet" type="text/css" href="http://www.gia.usb.ve/~alejandro/app/css/docs.css"/>
    <link rel="stylesheet" type="text/css" href="http://www.gia.usb.ve/~alejandro/app/css/style.css"/>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  </head>

<body>
<div class="grey">
<img src="http://www.gia.usb.ve/~alejandro/app/images/f.png" width=200 class="logo" alt="logo"/>
</div>

<h1><a href="."><span class=emph>Translated domain</span></a></h1>
<p class=sub> ICAPS'11 System Demos<br/>Translation of NP problems</p>

<!-- <h2> Instructions </h2>
<p> </p> -->

<div>
<pre class=grey>
""" + domain + error + """</pre></div>
<form action="translate2.py"  method="post">
</textarea>
    <div class=square>
    <center>
        <img src="http://www.gia.usb.ve/~alejandro/app/images/structureT.png" width=250/>
    </center>
    </div>
    <textarea name="structure" id="structure" cols="80" rows="20" type="text/html">
""" + structure + """</textarea>
    <input type="submit" value="Translate"/></div></form>

<div class=clear>
<a href="http://codemirror.net"><img src="http://www.gia.usb.ve/~alejandro/app/images/codemirror.png" height=70 class="align-right"/></a>
</div>
<div class=clear>
    <a href="http://gia.usb.ve"><img src="http://www.gia.usb.ve/~alejandro/app/images/gia-text.jpg" height=150 class="align-left"/></a>
    <a href="http://www.usb.ve"><img src="http://www.gia.usb.ve/~alejandro/app/images/usb-text.jpg" height=150 class="align-right"/></a>
</div>

    <!-- FINAL --> 
    <script type="text/javascript"> 
        var editor = CodeMirror.fromTextArea('formula', {
            parserfile: ["parsedct.js"],
            stylesheet: "codemirror/"http://www.gia.usb.ve/~alejandro/app/css/dctcolors.css",
            path: "codemirror/js/",
            lineNumbers: true,
            textWrapping: true,
            indentUnit: 4,
            parserConfig: {'pythonVersion': 2, 'strictErrors': true},
            tabMode: "spaces",
            autoMatchParens: true,
            height: "315px",
            markParen: "parentheses"
            // readOnly: true
        });
    </script> 
    <script type="text/javascript"> 
        var editor = CodeMirror.fromTextArea('signature', {
            parserfile: ["parsedct.js"],
            stylesheet: "codemirror/"http://www.gia.usb.ve/~alejandro/app/css/dctcolors.css",
            path: "codemirror/js/",
            lineNumbers: true,
            textWrapping: true,
            indentUnit: 4,
            parserConfig: {'pythonVersion': 2, 'strictErrors': true},
            tabMode: "spaces",
            autoMatchParens: true,
            height: "315px"
            // readOnly: true
        });
    </script> 
    <script type="text/javascript"> 
        var editor = CodeMirror.fromTextArea('structure', {
            parserfile: ["parsedct.js"],
            stylesheet: "codemirror/"http://www.gia.usb.ve/~alejandro/app/css/dctcolors.css",
            path: "codemirror/js/",
            lineNumbers: true,
            textWrapping: true,
            indentUnit: 4,
            parserConfig: {'pythonVersion': 2, 'strictErrors': true},
            tabMode: "spaces",
            autoMatchParens: true,
            height: "315px"
            // readOnly: true
        });
    </script> 
<!-- Dynamically change font  <script type="text/javascript" src="http://www.gia.usb.ve/~alejandro/app/css/font.js"></script> -->
  </body>
</html>
"""

print html_page

