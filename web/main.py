#!/usr/bin/env python

import cgi, cgitb, os, sys
cgitb.enable()
sys.path.insert(0, '/var/www/reductions')

#cgi.test()
print "Content-type: text/html\n\n"
page = """
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
<img src="http://www.google.com/images/logos/ps_logo2.png" width=200 class="logo" alt="logo"/>
</div>

<h1><a href="."><span class=emph>Second-order logic into STRIPS</span> Demo</a></h1>
<p class=sub> ICAPS'11 System Demos<br/>Translation of NP problems</p>

<div style="border: 3px solid black; padding: 0px;"> 
<form action="translate.py"  method="post">
    <div class=square>
    <center>
        <img src="images/formulaT.png" width=250/>
    </center>
    </div>
    <textarea name="formula" id="formula" cols="80" rows="20" type="text/html">
(so-exists (?T 1)
    (forall (?y)
        (exists (?x)
            (or
                (and (?P ?x ?y)
                     (?T ?x)
                )
                (and (?N ?x ?y)
                     (not (?T ?x))
                )
            )
        )
    )
)    
    </textarea>
    <div class=square>
    <center>
        <img src="images/signatureT.png" width=250/>
    </center>
    </div>
    <textarea name="signature" id="signature" cols="80" rows="20" type="text/html">
2
?P 2
?N 2
    </textarea>
    <input type="submit" value="Translate" />
</form>
</div> 

<!--
<div class="clear"><div class="left blk">
  <div class="clear"><div class="left1 blk">
    This is text from the left-1 block.
  </div><div class="left2 blk">
    This is text from the left-2 block.
  </div></div>

<h2 id="supported">This is a subtitle</h2>

</div>

<div class="right blk">
This is text from the right block.
</div>

</div>
-->

<div class=clear>
<a href="http://codemirror.net"><img src="images/codemirror.png" height=70 class="align-right"/></a>
</div>
<div class=clear>
    <a href="http://gia.usb.ve"><img src="images/gia-text.jpg" height=150 class="align-left"/></a>
    <a href="http://www.usb.ve"><img src="images/usb-text.jpg" height=150 class="align-right"/></a>
</div>

    <!-- FINAL --> 
    <script type="text/javascript"> 
        var editor = CodeMirror.fromTextArea('formula', {
            parserfile: ["parsedct.js"],
            stylesheet: "codemirror/css/dctcolors.css",
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
            stylesheet: "codemirror/css/dctcolors.css",
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
            stylesheet: "codemirror/css/dctcolors.css",
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
print page
