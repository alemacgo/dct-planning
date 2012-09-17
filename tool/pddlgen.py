from globals import *
#global_formulas, global_fluents, rel_symbols, initial_pddl_msg

def show_formulas():
    print "Formulas:"
    for i, formula in enumerate(global_formulas):
        print i
        formula.show()

def generate_fluents():
    new_fluents = set()
    variable_basename = "?x"
    for fluent in global_fluents:
        fluent = fluent.replace('(', '').replace(')', '').split()
        name = fluent[0]
        
        arguments = fluent[1:]

        for index, _ in enumerate(arguments):
            arguments[index] = variable_basename + str(index)

        fluent_str = "(" + name + " " + " ".join(arguments) + ")"
        new_fluents.add(fluent_str)

        if name.find('holds') == -1:
            global fluents_to_include
            fluents_to_include[name] = index+1
    return new_fluents

# testing
#def get_fluents():
#    fluent_list = []
#    for formula in global_formulas:
#        fluent = formula.get_fluent()
#        if fluent != None:
#            fluent_list.append(fluent)
#    return "\n\t" + "\n\t".join(fluent_list) + "\n"

# formula_tree should be the root of the syntax tree
def get_action_list(formula_tree):
    action_list = []
    for formula in global_formulas:
        actions = formula.get_actions()
        if actions != None: # atoms do not have associated actions
            action_list += actions

    goal_fluent = formula_tree.get_goal_action()
    # remember formula must be a sentence!

    # use ljust!
    dummy_action = "(:action begin-proof\n\t\t:precondition\t(guess)\n\t\t:effect\t\t(and (proof) (not (guess)))\n\t)"
    goal_action = "(:action prove-goal\n\t\t:precondition\t (and " +\
            goal_fluent + " (proof))\n\t\t:effect\t\t(holds_goal)\n\t)"
    action_list.append(dummy_action)
    action_list.append(goal_action)

    return "\n\t" + "\n\t".join(action_list) + "\n"  

def get_fluent_list():
    fluent_list = list(generate_fluents())
    fluent_list.sort()
    fluent_list.append("(guess)")
    fluent_list.append("(proof)")
    fluent_list.append("(holds_goal)")
    return "\t(:predicates\n\t\t" + "\n\t\t".join(fluent_list) + "\n\t)\n"

def get_constants():
    return "\t(:constants\n\t\tzero\n\t\tmax\n\t)\n\n"

def generate_pddl(pddl, domain_name, formula_tree):
    # begin pddl
    pddl.write(initial_pddl_msg)
    pddl.write("(define (domain " + domain_name + ")\n\n")

    actions = get_action_list(formula_tree)
    fluents = get_fluent_list() # fluents are gotten AFTER actions!
    constants = get_constants()

    pddl.write(constants)

    pddl.write(fluents)

    pddl.write(actions)

    # end pddl
    pddl.write(")")

    print "wrote pddl file"
    pddl.close()
              
