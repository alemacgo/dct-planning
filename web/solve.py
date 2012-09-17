#!/usr/bin/env python
import os
#os.system('echo > dct/output.out')
output = os.popen('../../experiments/planners/lama/plan dct/domain.pddl dct/problem.pddl dct/solution.out')
import cgi, cgitb, os
cgitb.enable()
print "Content-type: text/html\n\n"

html_page = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>Second-order logic into STRIPS</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="http://www.gia.usb.ve/~alejandro/app/css/plan.css"/>
  </head>

<body>
<!--<a href="check.py">Check for a solution</a>--></body></html>
""" + output.read().replace('\n','<br/>') + """</body><html>"""

print html_page
