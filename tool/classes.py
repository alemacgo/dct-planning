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

    def get_fluent(self, var = None, const = None):
        if len(self._childlist) < 2:
            return self._childlist[0].get_fluent()
            
        child = self._childlist[0]
        
        operator = child._info
        predicate = self._childlist[1]._childlist[0]._info
        predicate = predicate[1:] # remove the '?'
        
        if operator == soexists_keyword:
            fluent = "(holds_" + soexists_keyword + "_" + predicate + ")"
        elif operator == soforall_keyword:
            global_fluents.add(suc_fluent) #! manually add suc
            # regular forall fluent, called from outside
            fluent = "(holds_" + soforall_keyword + "_" + predicate + ")"
        else: pass # should not happen

        return fluent

    def collect_fluents(self):
        return [self.get_fluent()]
                
    # Find the fluent that activates the proof of the next subformula
    # in a metaforic way "pass the baton"
    # When begin generates de baton to pass to the first formula
    # otherwise, it selects the baton to pass to the next formula
    def get_baton(self, begin = False):
        baton = ""
        formula = ""
        if begin:
            formula = self
        else:
            formula = self._childlist[2]
        # print self._childlist[2]._childlist[0]
        if isinstance(formula._childlist[0], FoWff):
            # Fluent to be added at each action of foWff                
            baton = " (proof) "
        elif isinstance(formula._childlist[0], Operator):
            # Fluent to be added to let the subformula second order quantifiers start
            if formula._childlist[0]._info == soexists_keyword:
                childPredicate = formula._childlist[1]._childlist[0]._info[1:]
                baton = " (guess_" + childPredicate + ") "
            elif formula._childlist[0]._info == soforall_keyword:
                childPredicate = formula._childlist[1]._childlist[0]._info[1:]
                baton = " (iterate_" + childPredicate + ") (begin_so-forall_" + childPredicate + ") "
                global_fluents.add("(begin_so-forall_" + childPredicate + ")")
        return baton
        
    def get_soforall(self):
        prefix = "(:action "
        
        arity = self._childlist[1]._childlist[1]._info
        predicate = self._childlist[1]._childlist[0]._info
        predicate = predicate[1:] # remove the '?'
        
        variable = "?x"
        variables_list = []
        for i in range(arity):
            variables_list.append(variable + str(i))
        varList = " ".join(variables_list)
        
        coin_predicate = "coin_"+ predicate + " "
        free_condition = "(not_" + predicate + " " +\
                " ".join(variables_list) + ")"
        global_fluents.add("(" + coin_predicate + " ".join(variables_list) + ")")
        global_fluents.add(free_condition)
        
        baton = self.get_baton()
        mode = ""
        actions = ""
        
        iterateFluent = " (iterate_" + predicate + ") "
        global_fluents.add("(iterate_" + predicate + ")")
        suc_predicate = "(suc ?iv0 ?iv1)"
        care_condition = ""
        max_obj_predicate = ""
        max_parameter = "" #because the default is a constant (max) and does not need to be in the parameters
        zero_obj_predicate = ""
        zero_parameter = "" 
        max_obj = " max"
        zero_obj = " zero"
        aditional_prec_predicates = ""
        
        #If normal mode (not efficient one) ignores this if (possible better codification)
        if mode == "dont_care":
            care_predicate = "care_" + predicate + " "
            dont_care_predicate = "dont_care_" + predicate + " "
            dont_care_condition = " (or " + "(" + dont_care_predicate + (")(" + dont_care_predicate).join(variables_list) +")) "
            care_condition = " (and " + "(" + care_predicate + (")(" + care_predicate).join(variables_list) +"))"
            
            # Zero plus one dont care: pass to the next state of the relation whithout evaluate this one
            name = "zero_plus_one_dc_" + predicate
            parameters = ":parameters\t(" + " ".join(variables_list) + ")"
            precondition = ":precondition\t(and (" + coin_predicate + " ".join(variables_list) + ") "\
                                 + free_condition + "" + iterateFluent + " " + dont_care_condition + ")"
            effects = ":effect\t\t\t(and (not "+ free_condition + ") (" + predicate + " " + " ".join(variables_list) +"))\n\t)"
            global_fluents.add("(care_" + predicate + " ?x0)")
            global_fluents.add("(dont_care_" + predicate + " ?x0)")
            
            actions += "\n\t\t".join([prefix + name, parameters, precondition, effects]) + "\n\t"

        elif mode == "suc_special":
            #Need to block variables named iv*
            suc_predicate = " (so-forall_suc_" + predicate + " ?iv0 ?iv1)"
            max_obj_predicate = " (so-forall_max_" + predicate + " ?x0)"
            zero_obj_predicate = " (so-forall_zero_" + predicate + "?x0)"
            
            global_fluents.add(suc_predicate)
            global_fluents.add(max_obj_predicate)
            global_fluents.add(min_obj_predicate)
            max_obj = " ?ivmax"
            max_parameter = max_obj
            zero_obj = " ?ivzero"
            zero_parameter = zero_obj
            
            
            
            
        # Zero plus one
        name = "zero_plus_one_" + predicate
        parameters = ":parameters\t(" + " ".join(variables_list) + ")"
        precondition = ":precondition\t(and (" + coin_predicate + " ".join(variables_list) + ") "\
                             + free_condition + "" + iterateFluent + " " + care_condition + ")"
        effects = ":effect\t\t\t(and (not (" + coin_predicate + " ".join(variables_list) + ")) (not " +\
                            free_condition + ") (" + predicate + " " + " ".join(variables_list) +")" + baton + ")\n\t)"
        
        actions += "\n\t\t".join([prefix + name, parameters, precondition, effects]) + "\n\t"
        

        
        #One plus One base case
        name = "one_plus_one_0_" + predicate
        parameters = ":parameters\t(" + " ".join(variables_list[:-1]) + " ?iv0 ?iv1)" 
        precondition = ":precondition\t(and " + iterateFluent + "(" + coin_predicate + " ".join(variables_list[:-1]) + " ?iv0) ("\
                         + predicate + " " +  " ".join(variables_list[:-1]) + " ?iv0" + ") " + suc_predicate + " )"
        effects = ":effect\t\t\t(and (not (" + coin_predicate + " ".join(variables_list[:-1]) + " ?iv0)) "+\
                  "(not (" + predicate + " " + " ".join(variables_list[:-1]) + " ?iv0)) " +\
                  "(not_" + predicate + " " + " ".join(variables_list[:-1]) + " ?iv0) " +\
                  "(" + coin_predicate + " ".join(variables_list[:-1]) + " ?iv1) " + ")\n\t)"
                  
        actions += "\n\t\t".join([prefix + name, parameters, precondition, effects]) + "\n\t"
                            
        #One plus one n-ary relations
        for i in range(1,arity-1):
            name = "one_plus_one_" + str(i) + "_" + predicate
            parameters = ":parameters\t(" + " ".join(variables_list[:-i]) + "?iv0 ?iv1" + max_parameter + zero_parameter +")"
            precondition = ":precondition\t(and" + iterateFluent + "(" + coin_predicate + " ".join(variables_list[:-i]) + " ?iv0" + (i-1)*max_obj + ") (" + \
                             predicate + " " + " ".join(variables_list[:-i]) + " ?iv0" + (i-1)*max_obj + ") " + suc_predicate + max_obj_predicate + zero_obj_predicate + ")"
            effects = ":effect\t(and (not (" + coin_predicate + " ".join(variables_list[:-i]) + " ?iv0" + (i-1)*max_obj + ")) " +\
                       "(not ("+ predicate + " " + " ".join(variables_list[:-i]) + " ?iv0" + (i-1)*max_obj + ")) "+\
                      "(not_" + predicate + " "  + " ".join(variables_list[:-i]) + " ?iv0" + (i-1)*max_obj + ") " +\
                      "(" + coin_predicate + " ".join(variables_list[:-i]) + " ?iv1" + (i-1)*zero_obj + ") )\n\t)"
                      
            actions += "\n\t\t".join([prefix + name, parameters, precondition, effects]) + "\n\t"
        
        #Final case
        name = "one_plus_one_final_" + predicate
        parameters = ":parameters (" + max_parameter + ")"
        precondition = ":precondition\t(and" + iterateFluent + "("+ coin_predicate + arity*max_obj + ") (" + \
                         predicate + " " + arity*max_obj + max_obj_predicate +"))"
        effects = ":effect\t(and (not" + iterateFluent + ") (not (" + coin_predicate + arity*max_obj + ")) " +\
                   "(not ("+ predicate + " " + arity*max_obj + ")) " +\
                  "(not_" + predicate + " " + arity*max_obj + ") " +\
                  "(holds_so-forall_" + predicate + ") )\n\t)"
                  
        actions += "\n\t\t".join([prefix + name, parameters, precondition, effects]) + "\n\t"
        
        global_fluents.add("(holds_so-forall_" + predicate + ")")
        
        
        # If this is the final second order quantifier it needs delete
        # the proof fluent
        notProofFluent = ""
        if (baton == " (proof) "):
            notProofFluent = " (not (proof)) "
            
        # Action that increments the quantifier of the relation whith the condition
        # that the subformula has already been prooved with the current quantifier
        # state
        name = "change_for_coin_" + predicate
        parameters = ":parameters (" + zero_parameter + ")"   
        precondition = ":precondition\t(and" + iterateFluent + self._childlist[2].get_fluent() + zero_obj_predicate + ")"
        effects = ":effect\t(and" + notProofFluent + "(not " + self._childlist[2].get_fluent() + ")(coin_" + predicate + arity*zero_obj + ") )\n\t)"
        
        actions += "\n\t\t".join([prefix + name, parameters, precondition, effects]) + "\n\t"
        
        # Makes the proof of the quantifier when all the relations is false
        name = "init_so-forall_" + predicate        
        precondition = ":precondition\t(and" + iterateFluent + "(begin_so-forall_" + predicate + "))"
        effects = ":effect\t(and (not (begin_so-forall_" + predicate + "))" + baton + ")\n\t)"
        
        actions += "\n\t\t".join([prefix + name, precondition, effects])
        
        return [actions]
        
    def get_soexist(self):     
           
        inj = False
        func = False
        arity = self._childlist[1]._childlist[1]._info
        
        # @Dace: 9063340-45 - Situacion academica (Sencilla -18bsf - 5 dias habiles| rector 90bsf - 20 dias habiles)
        # Get predicate asosiated with the quantifier
        predicate = self._childlist[1]._childlist[0]._info
        predicate = predicate[1:] # remove the '?'
        
        if arity == 2: #Might be a function
            if predicate in func_symbols:
                func = True
            elif predicate in inj_symbols:
                inj = True
                
        # Getting parameters of the actions depending on the relation arity
        variable = "?x"
        variables_list = []
        for i in range(arity):
            variables_list.append(variable + str(i))
        parameters = ":parameters\t(" + " ".join(variables_list) + ")"

        # Constructing set_true and set_false actions
        prefix = "(:action "
        name_true = "set_true_" + predicate
        name_false = "set_false_" + predicate
        
        guessFluent = " (guess_" + predicate + ") "
        global_fluents.add("(guess_" + predicate + ")")
        # Find the fluent that activates the proof of the next subformula
        baton = self.get_baton()
                
        # Guess action separates the "guessing relations state" from
        # the "prove the subformula part". Method used for breaking symetries
        guess_action = "(:action end_guess_" + predicate + "\n\t\t" +\
                        ":precondition\t" + guessFluent + "\n\t\t" +\
                        ":effect\t\t(and" + baton + "(not" + guessFluent + "))\n\t)"
        
        free_condition = "(not_" + predicate + " " +\
                " ".join(variables_list) + ")"

        free_condition_functions = "(free_domain_" + predicate + " ?x0) "

        free_condition_injective = "(free_range_" + predicate + " ?x1) "
        
        #Set True
        precTrue = ":precondition\t(and " + free_condition + guessFluent
        effTrue = ":effect\t\t\t(and (" + predicate + " " + " ".join(variables_list)\
                    + ") (not " + free_condition + ") "
        #SetFalse
        precFalse = ":precondition\t(and (" + predicate + " " + " ".join(variables_list) + ") " + guessFluent
        effFalse = ":effect\t\t(and " + free_condition + " (not (" + predicate + " " + " ".join(variables_list) + "))   "
        
        #Adding constraints to make a relation work as a function or an injective function
        if inj or func: 
            #Adds for functions
            precTrue += free_condition_functions
            effTrue +=  "(not " + free_condition_functions + "))\n\t)"
            effFalse += free_condition_functions 
            global_fluents.add(free_condition_functions)
            
            if inj:
                #Adds for injective function            
                precTrue += "\n\t\t" + free_condition_injective
                effTrue += "\n\t\t(not " + free_condition_injective + ")"
                effFalse += free_condition_injective
                global_fluents.add(free_condition_injective)                        

        precTrue += ")"
        effTrue += ")\n\t)"
        
        precFalse += ")"
        effFalse += ")\n\t)"

        global_fluents.add(free_condition)
        
        strue = "\n\t\t".join([prefix + name_true, parameters, precTrue, effTrue])
        sfalse = "\n\t\t".join([prefix + name_false, parameters, precFalse, effFalse])
        
        #Establish so-exist -> used when the subformula of so-exist
        #is proved using a guessed relation
        notProofFluent = ""
        if (baton == " (proof) "):
            notProofFluent = " (not (proof)) "
            
        name = "establish_soexist_" + predicate        
        precondition = ":precondition\t(and " + self._childlist[2].get_fluent() + ")"
        effects = ":effect\t(and" + notProofFluent + "(not " + self._childlist[2].get_fluent() + ") (holds_" + soexists_keyword +\
                  "_" + predicate +")) \n\t)"
        finalAction = "\n\t\t".join([prefix + name, precondition, effects])

        global_fluents.add("(holds_" + soexists_keyword + "_" + predicate +")")

        return [strue + "\n\t" + sfalse + "\n\t" + guess_action + "\n\t" + finalAction]
        
    # make readable
    def get_actions(self):
        # not handling so-forall yet
        if self._childlist[0]._info == soforall_keyword:
            return self.get_soforall()
        else:
            return self.get_soexist()

        #! only handling existential quantification over one relation
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

	# def get_notAtoms_fluents(list):
		
		
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
            negFluents =[]
            for child in self._childlist:
                fluent = child.collect_fluents() 
                precondition_fluents += fluent  
                
                if fluent and fluent[0][1:7] == "holds_":
                    negFluents += [" (not " + fluent[0] + ")"]
                 
            # print precondition_fluents
            prec = ":precondition\t(and " + " ".join(precondition_fluents) + " (proof))"
            
            eff = ":effect\t\t(and " + self.get_fluent() + " " + " ".join(negFluents) + ")\n\t)"
            return ["\n\t\t".join([prefix + name, parameters, prec, eff])]
        elif operator == or_keyword:
            precondition_fluents = []
            
            for child in self._childlist:
                precondition_fluents += child.collect_fluents() 

            name = "establish_or_" + str(self.id)
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) + ")"
            

            operator_list = []
            for index, fluent in enumerate(precondition_fluents):
                prec = ":precondition\t (and " + fluent + " (proof))"
                negFluent = ""
                if fluent[1:7] == "holds_":
                    negFluent =" (not " + fluent + ")"
                eff = ":effect\t\t(and " + self.get_fluent() + negFluent + ")\n\t)"
                operator_list.append("\n\t\t".join([prefix + name +\
                        "_" + str(index), parameters, prec, eff]))

            return operator_list
        elif operator == exists_keyword:
            # only one-variable exists for now
            quantified_variable = self._childlist[1]._childlist[0]._info

            name = "establish_exists_" + str(self.id)
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) +\
                    " " + quantified_variable + ")" # added quantified var

            childFluents = self._childlist[2].get_fluent() 
            negFluent = ""
            if childFluents[1:7] == "holds_":
                negFluent =" (not " + childFluents + ")"
            prec = ":precondition\t (and " + childFluents + " (proof))"
            eff = ":effect\t\t(and "+ self.get_fluent() + negFluent + "))"

            return ["\n\t\t".join([prefix + name, parameters, prec, eff])]
        elif operator == forall_keyword:
            quantified_variable = self._childlist[1]._childlist[0]._info

            childFluentsBase = self._childlist[2].get_fluent(quantified_variable, zero_keyword)
            print childFluentsBase
            negFluentBase = ""
            if childFluentsBase[1:7] == "holds_":
                negFluentBase =" (not " + childFluentsBase + ")"
                
            name = "establish_forall_" + str(self.id) + "_base"
            parameters = ":parameters\t(" + " ".join(self.free_vars_set) + ")"
            prec = ":precondition\t (and " + childFluentsBase + " (proof))"
            eff = ":effect\t\t(and " + self.get_forall_fluent(quantified_variable, zero_keyword) +\
 				  " " + negFluentBase + ")\n\t)"
			
            fluent_1 = "\n\t\t".join([prefix + name, parameters, prec, eff])

            name = "establish_forall_" + str(self.id) + "_inductive"

            # Variables iv0 and iv1 represent two steps
            # of the induction, where suc(iv0) = iv1

            childFluentsInduc_1 = self.get_forall_fluent(quantified_variable, "?iv0")
            childFluentsInduc_2 = self._childlist[2].get_fluent(quantified_variable, "?iv1")

            negFluentInduc_1 = ""
            if childFluentsInduc_1[1:7] == "holds_":
                negFluentInduc_1 =" (not " + childFluentsInduc_1 + ")"
                
            negFluentInduc_2 = ""
            if childFluentsInduc_2[1:7] == "holds_":
                negFluentInduc_2 =" (not " + childFluentsInduc_2 + ")"

            parameters = ":parameters\t(" + " ".join(self.free_vars_set) +\
                    " ?iv0 ?iv1)"
            prec = ":precondition\t(and " + childFluentsInduc_1 + " (suc ?iv0 ?iv1) " + \
                    childFluentsInduc_2 + " (proof))"

            eff = ":effect\t\t(and " + negFluentInduc_1 + " " + negFluentInduc_2 + " " +\
                    self.get_forall_fluent(quantified_variable, "?iv1") + ")\n\t)"

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
