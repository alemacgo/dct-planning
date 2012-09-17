#! /usr/bin/env python
from sys import argv
import os, parser, pddlgen, globals # remove classes after testing

usage = """
usage:
    soplan [flags] <input_file> [<signature_file>]

flags:
    --silent
    --nocolor:
        Don't colorize output.
    --output=path:
        Send output PDDL file to this location
    --problem=path:
        Translate the domain and instance in this location
"""

try:
    # default settings
    colors = True
    output_path = None
    problem_path = None
    silence = False

    option = 1 # current command-line option
    flag = argv[option]

    while flag[:2] == "--":
        print flag
        if flag == "--nocolor": 
            colors = False
        elif flag == "--silent":   # to implement!
            silence = True
        elif flag[:8] == "--output":
            output_path = flag[9:]
        elif flag[:9] == "--problem":
            problem_path = flag[10:]
        else:
            raise SystemExit("unknown flag '%s'. \n%s" %(flag, usage))
        option += 1
        flag = argv[option]

    # opening main prenex file
    file_path = argv[option]
    try:
        prenex_file = open(file_path).readlines()
    except IOError, e:
        raise SystemExit("Error reading file: %s\nReason: %s." %(e.filename, e))  

    file_path = file_path.rpartition(".")[0] # without extension
    filename = file_path.split('/')[-1]

    # attempting to open its signature file
    try:
        signature = open(file_path + ".sig").readlines()
        parser.read_signature(signature)
    except IOError:
        print "warning: no signature file found"
    except parser.SignatureError, e:
        print "warning (signature error): %s" %(e.msg)

except IndexError:
    raise SystemExit(usage)
    
#print parser.inj_symbols
#print parser.symbols

tokens = parser.tokenize(prenex_file)

# attempt to parse main file
try:
    syntax_tree = parser.parse(tokens)

except parser.SyntaxError, e:
    error = "In line: %d, syntax error: Got '%s', expected '%s'.\n"\
    %(e.lineNumber, e.got, e.expected)
    if e.msg != None:
        error += "\t%s" %(e.msg)
    raise SystemExit(error)
            
except parser.DefinitionError, e:
    raise SystemExit("In line: %d, definition error: %s.\n" %(e.lineNumber, e.msg))

except parser.ArityError, e:
    raise SystemExit("In line: %d, arity error: %s.\n" %(e.lineNumber, e.msg))

except parser.TokenExcessError, e:
    raise SystemExit("In line %d, syntax error; unexpected token: '%s'.\n"\
            %(e.lineNumber, e.got))

except StopIteration, e:
    raise SystemExit("Syntax error: check for missing closing brackets.")

syntax_tree.assign_free_variables()
syntax_tree.push_negations(False)

if colors:
    syntax_tree.show()
else:
    syntax_tree.showBW()

#parser.show_symbol_table()
syntax_tree.get_logical_formulas()

#pddlgen.show_formulas()
print output_path
if output_path: pddl_file = open(output_path, "w")
else: pddl_file = open(file_path + ".pddl", "w")

pddlgen.generate_pddl(pddl_file, filename, syntax_tree)

if problem_path:
    os.system('./problemGenerator.py ' + problem_path + " '" +\
            str(globals.fluents_to_include) + "'" + " '" +\
            str(globals.quantified_relations) + "'" + " '" +\
            filename + "'")

