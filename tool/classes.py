DEBUG = False
#DEBUG = True

# Parser for second-order logic in prenex form
# Implementation
# TODO:
#       Possibly catch more types of syntax errors (and 1(...
#       Check assign_free_variables_set readability/efficiency

from globals import *

# Classes
"""
SyntaxTree: 
General tree (a tree in which every node may have zero or more children).
A (concrete) SyntaxTree is one of these two kinds of nodes:
(SyntaxTree) Nodes without information, with represent non-terminal symbols in
    the formal grammar, with a non-empty list of children.
    These nodes have self._info == None.
(Leaf) Nodes with information, which represent terminal
    symbols in the formal grammar.
    These nodes have self._info != None, and self.childlist == None.
"""
class SyntaxTree:
    node_type = ''
    """
    node_type is a class attribute for Type 1 nodes that holds
    the "name" of the non-terminal in the formal grammar.
    """

    def __init__(self, childlist = None):
        self._childlist = childlist
        self._info = None

    """
    After parsing, this helper method determines
    whether the tree has been succesfully built,
    or there was an uncatched syntax error
    """
    def check_consistency(self):
        if not self._childlist == None:
            for child in self._childlist:
                # caused by an empty argument list after an operator
                if child == None: 
                    raise SyntaxError(lineNumber, ")", "<VAR>|<CONST>")
                child.check_consistency()

    """
    Procedures for printing the structure of a tree
    to the console.
    The show method colorizes output, the showBW method doesn't.
    """
    def _show(self, depth, color = True):
        print depth*" |    " + self.node_type  # show itself
        for child in self._childlist: # show its children
            child._show(depth + 1, color)
        
    def show(self):
        self._show(0)

    def showBW(self):
        self._show(0, False)

#    def __str__(self):
#        if self._info != None:
#            return self._info
#        else:
#            return "." + str(self._childlist)

    def _restart(self, tree):
        self._info = tree._info
        self._childlist = tree._childlist

    def push_negations(self, propagation):
        if self._childlist != None:
            for child in self._childlist:
                child.push_negations(propagation)

    def assign_free_variables(self):
        for i in self._childlist:
            i.assign_free_variables()
        return set()
            
    def get_logical_formulas(self):
        if not self._childlist == None:
            for child in self._childlist:
                child.get_logical_formulas()

class Leaf(SyntaxTree):
    def _show(self, depth, color = True):
        if color:
            print depth*" |    " + color_blue + self.node_type + ": "\
                + color_green + str(self._info) +\
                color_normal   
        else:
            print depth*" |    " + self.node_type + ": "\
                + str(self._info)

    def __init__(self, info):
        SyntaxTree.__init__(self)
        self._info = info

    def check_consistency(self):
        pass

    def assign_free_variables(self): 
        return set()  

"""
SubFormula: 
Nodes containing formulas whose set of free variables can
be calculated
"""
# Formulas whose set of free variables can be calculated
class SubFormula(SyntaxTree):
    def __init__(self, childlist = None):
        SyntaxTree.__init__(self, childlist)
        self.free_vars_set = set()

"""
LogicalFormula: 
Formulas that will be translated into fluents and actions
"""
class LogicalFormula(SubFormula):
    def __init__(self, childlist = None):
        SubFormula.__init__(self, childlist)
        global nodeNumber
        self.id = nodeNumber
        nodeNumber += 1
        
    def get_logical_formulas(self):
        global_formulas.append(self)
        SyntaxTree.get_logical_formulas(self)

    if DEBUG:
        """
        This show method also displays free variables associated
        to each node and node number, for debugging
        """
        def _show(self, depth, color = True):
            if self._info == None:
                print depth*" |    " + self.node_type + " " + str(self.free_vars_set)\
                + " [" + color_red + str(self.id) + color_normal + "]"
            else:
                print depth*" |    " + SyntaxTree.color_blue + self.node_type +\
                        SyntaxTree.color_green + str(self._info) + SyntaxTree.color_normal\
                        + " " + str(self.free_vars_set) + " [" + str(self.id) + "]"
            
            if not self._childlist == None:
                for child in self._childlist:
                    child._show(depth + 1, color)
        
# Concrete data types
class SoWff(LogicalFormula):
    node_type = "<so-wff>"

    def assign_free_variables(self):
        for i in self._childlist:
            self.free_vars_set |= i.assign_free_variables()
        return self.free_vars_set

    # only second-order quantifiers need to be added to the formulas list
    def get_logical_formulas(self):
        if self._childlist[0]._info in so_wff:
            global_formulas.append(self)
        for child in self._childlist:
            child.get_logical_formulas()

    def get_fluent(self):
        return None # so-wff has no fluents associated

    # make readable
    def get_actions(self):
        # not handling so-forall yet
        if self._childlist[0]._info == soforall_keyword:
            return ""
        #! only handling existential quantification over one relation

        prefix = "(:action "
        name_true = "set_true_" + str(self.id)
        name_false = "set_false_" + str(self.id)
        
        inj = False
        func = False
        arity = self._childlist[1]._childlist[1]._info
        predicate = self._childlist[1]._childlist[0]._info
        
        if arity == 2: #Might be a function
            if predicate in func_symbols:
                func = True
            elif predicate in inj_symbols:
                inj = True
        
        predicate = predicate[1:] # remove the '?'
        
        variable = "?x"
        variables_list = []
        for i in range(arity):
            variables_list.append(variable + str(i))

        #! remove free variable association from SoWff!
        parameters = ":parameters\t(" + " ".join(variables_list) + ")"

        #Modification N#3 -> Change (free_f x y) for (not_f x y) and remove set_false action
        #free_condition = "(free_" + predicate + " " +\
        #        " ".join(variables_list) + ")"
        
        #We assume that the free condition is the predicate assigned to false
        free_condition = "(not_" + predicate + " " +\
                " ".join(variables_list) + ")"

        #! to avoid f(zero, ?x) and f(zero, ?y) where ?x != ?y
        free_condition_functions = "(free_domain_" + predicate + " ?x0)"

        #! to avoid f(?x, zero) and f(?y, zero) where ?x != ?y
        free_condition_injective = "(free_range_" + predicate + " ?x1)"

        #TODO FIX
        
        if inj: #it's an injective function
            precTrue = ":precondition\t(and " + free_condition + "\n\t\t" +\
            free_condition_functions + "\n\t\t" + free_condition_injective +\
            " (guess))"
            eff_true = ":effect\t\t\t(and (" + predicate + " ?x0 ?x1)\n\t\t(not " +\
            free_condition + " ) (not " + free_condition_functions + " )\n\t\t(not " +\
            free_condition_injective + "))\n\t)"
            global_fluents.add(free_condition_injective)                        
            global_fluents.add(free_condition_functions)
        elif func: #it's a regular function CHECK! NOT TESTED
            precTrue = ":precondition\t(and " + free_condition +\
                    " " + free_condition_functions +\
                        " (guess))"
            eff_true = ":effect\t\t(and (" + predicate + " ?x0 ?x1) (not " + free_condition +\
                        ") (not " + free_condition_functions + "))\n\t)"
            global_fluents.add(free_condition_functions)
        else: # it's a relation
            arity = int(arity)
            precTrue = ":precondition\t(and " + free_condition + " (guess))"
            eff_true = ":effect\t\t(and (" + predicate + " " + " ".join(variables_list)\
                        + ") (not " + free_condition + "))\n\t)"

        #negated_predicate_fluent = "(not_" + predicate + " " +\
        #        str(" ".join(variables_list)) + ")"
        #print negated_predicate_fluent
        #
        #global_fluents.add(negated_predicate_fluent)

        #eff_false = ":effect\t\t(and " + negated_predicate_fluent +\
        #        " (not " + free_condition + "))\n\t)"
        #
        #precFalse = ":precondition\t (and (" + free_condition + ") (guess))"
        global_fluents.add(free_condition)
        
        strue = "\n\t\t".join([prefix + name_true, parameters, precTrue, eff_true])
        #Set False ommited because the modification N#3 -> More efficient
        #sfalse = "\n\t\t".join([prefix + name_false, parameters, precFalse, eff_false])
        #print "\ninj_symbols:"
        #print inj_symbols
        #print "\nfunc_symbols:"
        #print func_symbols
        return [strue]
        #return [strue, sfalse]

    def get_goal_action(self):
        if self._childlist != None: 
            for child in self._childlist:
                action = child.get_goal_action()
                if action != None:
                    return action

class FoWff(LogicalFormula):
    node_type = "<fo-wff>"

    def push_negations(self, propagation):
        childlist = self._childlist
        first_child = childlist[0]
        child_keyword = first_child._info
        if not childlist == None:
            if propagation:
                if isinstance(first_child, Atom): # must negate this atom
                    not_node = Operator(not_keyword)
                    new_childlist = []
                    new_childlist.append(Operator(not_keyword))
                    new_childlist.append(first_child)
                    self._childlist = new_childlist 

                elif child_keyword in nary_operators or \
                     child_keyword in fo_wff:
                    first_child.complement() # switch and to or...
                    for child in self._childlist:
                        child.push_negations(True)   
                elif child_keyword == not_keyword:
                    self._restart(childlist[1]) # assign next->next formula to self
                    self.push_negations(False) # stop propagation
                    # this removes double negations
                else:
                    for descendent in descendentlist:
                        descendent.push_negations(True)

            elif child_keyword == not_keyword: # 'not' detected, begin propagation
                self._restart(childlist[1])
                self.push_negations(True)
            else: # everything positive, go down to the next level
                for child in childlist:
                    child.push_negations(propagation)  

    def assign_free_variables(self):
        if self._childlist[0]._info in fo_wff:
            list_var = (self._childlist[1]).assign_free_variables()
            for i in range(2, len(self._childlist)):
                self.free_vars_set |= (self._childlist[i]).assign_free_variables()
                self.free_vars_set -= list_var
            return self.free_vars_set
        elif self._childlist[0]._info in nary_operators or \
                self._childlist[0]._info in unary_operators:
            for i in range(1, len(self._childlist)):
                self.free_vars_set |= (self._childlist[i]).assign_free_variables()
            return self.free_vars_set
        else:
            self.free_vars_set |= (self._childlist[0]).assign_free_variables()
            return self.free_vars_set

    ## improve readability
    def get_fluent(self, var = None, const = None):
        child = self._childlist[0]
        operator = child._info

        # possibly instantiate the argument list
        if isinstance(child, Atom): 
            argument_list = instantiate(child.args_list, var, const) # atoms are handled diff
        # quick hack to make it work with negative atoms!
        # more testing required
        elif operator == not_keyword: 
            atom = self._childlist[1]
            argument_list = instantiate(atom.args_list, var, const)
        else: argument_list = instantiate(list(self.free_vars_set), var, const)

        if isinstance(child, Atom):
            relation = child._childlist[0]

            ## if the relation is predefined, handle it here!
            if relation._info in predefined_relations:
                fluent = get_relation_fluent(relation._info, argument_list)
            else:
                fluent = "(" + relation._info[1:] +\
                         " " + " ".join(argument_list) + ")"
                global_fluents.add(fluent)

        elif operator == not_keyword:
            atom = self._childlist[1]
            relation = atom._childlist[0]

            ## if the relation is predefined, handle it here!
            if relation._info in predefined_relations:
                fluent = get_relation_neg(relation._info, argument_list)
            else:
                fluent = "(not_" + relation._info[1:] +\
                         " " + " ".join(argument_list) + ")"
                global_fluents.add(fluent)

        elif operator in nary_operators or operator == exists_keyword:
            fluent = "(holds_" + operator + "_" + str(self.id) +\
                     " " + " ".join(argument_list) + ")"
            global_fluents.add(fluent)

        elif operator == forall_keyword:
            global_fluents.add(suc_fluent) #! manually add suc
            # regular forall fluent, called from outside
            fluent = "(holds_" + operator + "_" + str(self.id) +\
                    " " + " ".join(argument_list) + " " +\
                     max_keyword + ")"
            global_fluents.add(fluent)
        else: pass # should not happen

        return fluent

    # new
    # intended to be used with ?iv1 or zero
    def get_forall_fluent(self, var, const):
        argument_list = instantiate(list(self.free_vars_set), var, const)
        if argument_list:
            fluent = "(holds_forall_" + str(self.id) +\
                     " " + " ".join(argument_list) + " " +\
                    const + ")"
        else: fluent = "(holds_forall_" + str(self.id) + " " + const + ")"

        #global_fluents.add(fluent)
        return fluent

    def collect_fluents(self):
        return [self.get_fluent()]
        
    def get_actions(self):
        child = self._childlist[0]
        operator = child._info

        prefix = "(:action "

        if isinstance(child, Atom) or operator == not_keyword:
            return None
        elif operator == and_keyword:
            name = "establish_and_" + str(self.id)
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) + ")"

            precondition_fluents = []
            for child in self._childlist:
                precondition_fluents += child.collect_fluents() 

            prec = ":precondition\t(and " + " ".join(precondition_fluents) + " (proof))"

            eff = ":effect\t\t" + self.get_fluent() + "\n\t)"
            return ["\n\t\t".join([prefix + name, parameters, prec, eff])]
        elif operator == or_keyword:
            precondition_fluents = []
            for child in self._childlist:
                precondition_fluents += child.collect_fluents() 

            name = "establish_or_" + str(self.id)
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) + ")"
            eff = ":effect\t\t" + self.get_fluent() + "\n\t)"

            operator_list = []
            for index, fluent in enumerate(precondition_fluents):
                prec = ":precondition\t (and " + fluent + " (proof))"
                operator_list.append("\n\t\t".join([prefix + name +\
                        "_" + str(index), parameters, prec, eff]))

            return operator_list
        elif operator == exists_keyword:
            # only one-variable exists for now
            quantified_variable = self._childlist[1]._childlist[0]._info

            name = "establish_exists_" + str(self.id)
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) +\
                    " " + quantified_variable + ")" # added quantified var

            prec = ":precondition\t (and " + self._childlist[2].get_fluent() + " (proof))"
            eff = ":effect\t\t" + self.get_fluent() + "\n\t)"

            return ["\n\t\t".join([prefix + name, parameters, prec, eff])]
        elif operator == forall_keyword:
            quantified_variable = self._childlist[1]._childlist[0]._info

            name = "establish_forall_" + str(self.id) + "_base"
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) + ")"
            prec = ":precondition\t (and " + \
                    self._childlist[2].get_fluent(quantified_variable, zero_keyword) + " (proof))"
            eff = ":effect\t\t" + \
                    self.get_forall_fluent(quantified_variable, zero_keyword) + "\n\t)"

            fluent_1 = "\n\t\t".join([prefix + name, parameters, prec, eff])

            name = "establish_forall_" + str(self.id) + "_inductive"

            # Variables iv0 and iv1 represent two steps
            # of the induction, where suc(iv0) = iv1
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) +\
                    " ?iv0 ?iv1)"
            prec = ":precondition\t(and " + \
                    self.get_forall_fluent(quantified_variable, "?iv0") +\
                    " (suc ?iv0 ?iv1) " + \
                    self._childlist[2].get_fluent(quantified_variable, "?iv1") + \
                    " (proof))"

            eff = ":effect\t\t" + \
                    self.get_forall_fluent(quantified_variable, "?iv1") + "\n\t)"

            fluent_2 = "\n\t\t".join([prefix + name, parameters, prec, eff])

            return [fluent_1, fluent_2]

        return None

    def get_goal_action(self):
        return self.get_fluent()

class ListFoWff(SubFormula):
    node_type = "<list-fo-wff>"

    def assign_free_variables(self):
        for i in self._childlist:
            self.free_vars_set |= i.assign_free_variables()
        return self.free_vars_set

    def collect_fluents(self):
        precondition_fluents = []
        for child in self._childlist:
            precondition_fluents += child.collect_fluents() 
        return precondition_fluents
        
class Atom(SubFormula):
    node_type = "<atom>"
    
    def __init__(self, childlist = None):
        SubFormula.__init__(self, childlist)
        self.args_list = []

    # push negations no further, for efficiency
    def push_negations(self, propagation):
        pass

    def assign_free_variables(self):
        self.args_list += self._childlist[1].argument_list()
        # self.free_vars_set |= set(self.args_list) # problems! constants get in
        #print self.args_list

        for i in self._childlist:
            self.free_vars_set |= i.assign_free_variables()
        return self.free_vars_set

#    def return_instantiated(variable, constant):
#        new_atom = copy.deepcopy(self)
#        for child in new_atom._childlist[1:]:
#            child.instantiate(variable, constant)
    
# no need for implementing this now, <list-term> goes directly to Var|Const
#class Term(SyntaxTree):
#    node_type = "<term>"
#
#    def assign_free_variables(self):
#        list_var = set()
#        for i in self._childlist:
#            list_var |= i.assign_free_variables()
#        return list_var
    
class ListRel(SyntaxTree):
    node_type = "<list-rel>"

    # push negations should be ignored for efficiency at this level
    def push_negations(self, propagation):
        pass

    def get_goal_action(self):
        pass

class ListVar(SyntaxTree):
    node_type = "<list-var>"

    def __init__(self, childlist = None):
        SyntaxTree.__init__(self, childlist)
        self.variables = set() # set of variables being held by this ListVar

    if DEBUG:
        # instead of showing every node down this branch, just show
        # the variable list in a compact format
        def _show(self, depth, color = True):
            print depth*" |    " + self.node_type + " " + color_yellow +\
                    str(list(self.variables)) + color_normal

    def assign_free_variables(self):
        list_var = set()
        for i in self._childlist:
            list_var |= i.assign_free_variables()
        self.variables = list_var
        return list_var

class ListTerm(SyntaxTree):
    node_type = "<list-term>"

    def assign_free_variables(self):
        list_var = set()
        for i in self._childlist:
            list_var |= i.assign_free_variables()
        return list_var

    def argument_list(self):
        if len(self._childlist) == 1:
            return [self._childlist[0]._info]
        return [self._childlist[0]._info] + self._childlist[1].argument_list()

#    def instantiate(variable, constant):
#        if self._childlist[0]._info == variable:
#            self._childlist[0] = Const(constant)
#        if len(self._childlist) > 1:
#            self._childlist[1].instantiate()

class Var(Leaf):
    node_type = "<VAR>"

    def assign_free_variables(self): 
        return set([self._info])

class Const(Leaf):
    node_type = "<CONST>"

class Rel(Leaf):
    node_type = "<REL>"
    
class Func(Leaf):
    node_type = "<FUNC>"

class Int(Leaf):
    node_type = "<int>"
    
class Operator(Leaf):
    def _show(self, depth, color = True):
        if color:
            print depth*" |    " + color_green + self._info + color_normal
        else:
            print depth*" |    " + self._info

    def complement(self):
        if self._info == and_keyword: self._info = or_keyword
        elif self._info == or_keyword: self._info = and_keyword
        elif self._info == forall_keyword: self._info = exists_keyword
        elif self._info == exists_keyword: self._info = forall_keyword 

    def assign_free_variables(self): 
        return set()  

    def collect_fluents(self):
        return []

    def get_goal_action(self):
        pass

class SyntaxError(Exception):
    def __init__(self, lineNumber, got, expected, msg = None):
        self.lineNumber = lineNumber
        self.got = got
        self.expected = expected
        self.msg = msg

class DefinitionError(Exception):
    def __init__(self, lineNumber, message):
        self.lineNumber = lineNumber
        self.msg = message
        
class ArityError(Exception):
    def __init__(self, lineNumber, numberOfVars, got):
        self.lineNumber = lineNumber
        
        if numberOfVars == 0:
            self.msg = "expected no more variables after '%s'" %(got)
        else:
            def add_final_s(n):
                if n == 1: return ""
                else: return "s"

            self.msg = "expected %d more variable%s after '%s'" \
                    %(numberOfVars, add_final_s(numberOfVars), got) 

class TokenExcessError(Exception):
    def __init__(self, lineNumber, got):
        self.lineNumber = lineNumber
        self.got = got

class SignatureError(Exception):
    def __init__(self, msg):
        self.msg = msg
