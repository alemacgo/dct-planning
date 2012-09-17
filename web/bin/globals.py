# Module globals
# Global variables for defining and controlling the parser

import re

# Constants for the prenex grammar
forall_keyword = 'forall'
exists_keyword = 'exists'
soforall_keyword = 'so-forall'
soexists_keyword = 'so-exists'
so_wff = [soforall_keyword, soexists_keyword] # second-order logic quantifiers
fo_wff = [forall_keyword, exists_keyword] # first-order logic quantifiers

and_keyword = 'and'
or_keyword = 'or'
not_keyword = 'not'
implies_keyword = 'implies'
nary_operators = [and_keyword, or_keyword, implies_keyword] # n-ary and binary logic relations 
unary_operators = [not_keyword] # unary logic relations

predefined_relations = ['<', '<=', '>=', '>', '=', 'suc']
func_symbols = set()
inj_symbols = set()

# Symbol table
# These tuples mean (arity, type), where type = 0 if rel is a relation,
#                                             = 1 if rel is a function,
#                                             = 2 if rel is an injective function
all_symbols = {'<': (2, 0), '<=': (2, 0), '>': (2, 0), '>=': (2, 0), \
        'suc': (2, 0), '=' : (2, 0)}
symbols = {'suc': (2,0)}

# Final symbol table with the fluents to include (which can be used in the
# instance or be automatically generated)
# [(symbol, arity)]
# e.g. [(not_k, 1), (k, 1), (e, 2)]
fluents_to_include = {}

quantified_relations = {}

# Set of constants defined in the signature file
max_keyword = "max"
zero_keyword = "zero"
constants_set = set([max_keyword, zero_keyword])

# Regular expressions for defining the terminal symbols
variables = re.compile("\A\?[a-z]\w*\Z")
integers = re.compile("\A-?\d+\Z")
relations = re.compile("\A(\?[a-z]\w*|" + '|'.join(predefined_relations) + ')\Z')
constants = re.compile("\A(" + '|'.join(constants_set) + ')\Z')  # quick, remove later
#functions = re.compile("\A[a-z]\w*\Z")
constants = re.compile("\A(" + "|".join(constants_set) + ")\Z")

# Constants for pretty-printing a SyntaxTree
color_red = '\033[1;31m'
color_blue = '\033[1;34m'
color_green = '\033[1;32m'
color_yellow = '\033[1;33m'
color_normal = '\033[0m'  

# Constant fluents for predefined relations
lt_fluent = "(lt ?x0 ?x1)"
gt_fluent = "(gt ?x0 ?x1)"
suc_fluent = "(suc ?x0 ?x1)"

def get_relation_fluent(relation, argslist):
    if relation == "=": return "(= " + " ".join(argslist) + ")"
    elif relation == "<": 
        global_fluents.add(lt_fluent)
        return "(lt " + " ".join(argslist) + ")"
    elif relation == ">":
        global_fluents.add(gt_fluent)
        return "(gt " + " ".join(argslist) + ")"
    elif relation == "<=": 
        global_fluents.add(lt_fluent)
        return "(or (lt " + " ".join(argslist) + ")" +\
                  " (= " + " ".join(argslist) + "))"
    elif relation == ">=": 
        global_fluents.add(gt_fluent)
        return "(or (gt " + " ".join(argslist) + ")" +\
                  " (= " + " ".join(argslist) + "))"
    elif relation == "suc": 
        global_fluents.add(suc_fluent)
        return "(suc " + " ".join(argslist) + ")"
    else: raise ValueError

# gets the complement of the relation
def get_relation_neg(relation, argslist):
    if relation == "=": return "(not (= " + " ".join(argslist) + "))"
    elif relation == "<": 
        global_fluents.add(gt_fluent)
        return "(or (gt " + " ".join(argslist) + ")" +\
                  " (= " + " ".join(argslist) + "))"   
    elif relation == ">":
        global_fluents.add(lt_fluent)
        return "(or (lt " + " ".join(argslist) + ")" +\
                  " (= " + " ".join(argslist) + "))"
    elif relation == "<=": 
        global_fluents.add(gt_fluent)
        return "(gt " + " ".join(argslist) + ")"
    elif relation == ">=": 
        global_fluents.add(lt_fluent)
        return "(lt " + " ".join(argslist) + ")"  
    #elif relation == "suc": return "(suc ?x0 ?x1)"
    else: raise ValueError

#def simplify_comparison_operators(fluent_list):
#    for i, elem in enumerate(fluent_list):
#        if elem == "(leq ?x0 ?x1)":
#            fluent_list[i] = ("(or (lt ?x0 ?x1) (= ?x0 ?x1))")
#        elif elem == "(geq ?x0 ?x1)":
#            fluent_list[i] = ("(or (gt ?x0 ?x1) (= ?x0 ?x1))")

# implementing support for constants later
#def get_constants_set():
#    global constants_set
#    global constants
#    constants_set.add("LAMA")
#    constants = re.compile("\A(" + "|".join(constants_set) + ")\Z")

# Line number the parser is currently analyzing
lineNumber = 0

# Node number the parser is currently building
nodeNumber = 0

# This list will contain the LogicalFormulas
global_formulas = []

# This set will contain fluents referenced by one or more actions
global_fluents = set()

# Function to 'instantiate' all ocurrences of a variable in a list
# This is useful for the 'forall' fluents
def instantiate(args, var = None, const = None):
    if var == None and const == None:
        return args
    #print var, const
    new_args = args[:]
    for index, argument in enumerate(new_args):
        if argument == var:
            new_args[index] = const
    return new_args

# Initial message to write in the PDDL file
initial_pddl_msg = \
""";;; Auto-generated PDDL file from prenex formula

"""

