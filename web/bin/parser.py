from classes import *

def tokenize(input):
    for line in input:
        global lineNumber
        lineNumber += 1
        line = line.partition(";")[0]
        line = line.replace('(', ' ( ').replace(')', ' ) ')
        for token in line.split():
            yield token.lower()

def get_excess_token(tokens):
    try:
        n = tokens.next()
    except StopIteration:
        return None
    return n

def read_signature(signature):
    # reading relations
    # print signature
    try:
        number_of_relations = int(signature[0])
    except ValueError:
        raise SignatureError(
        "the first non-whitespace character should be an integer"
        + " with the number of relations in the signature file")
    for index in range(1, number_of_relations + 1):
        line = signature[index]
        line = line.split(";", 1)[0]  # strip comments
        line = line.replace('(', '').replace(')', '').split()
        try:
            arity = line[1]
            rel_name = line[0].lower()
            if symbols.has_key(rel_name):
                raise SignatureError("relation '%s' already defined" %(rel_name))

            # print rel_name
            # print arity
            if arity != 'inj' and arity != 'func': #Relation is not a function
                symbols[rel_name] = (int(line[1]), 0)
            else: #Relation is a function
                if arity == 'inj':      #Injective function
                    symbols[rel_name] = (2, 2)
                    inj_symbols.add(rel_name)
                else:                   #Regular function
                    symbols[rel_name] = (2, 1)
                    func_symbols.add(rel_name)
    
        except IndexError:
            raise SignatureError("wrong formatting")
        except ValueError:
            raise SignatureError("unexpected token '%s'." %(line[1]))
    
    # reading constants
    # to be implemented
#    try:
#        number_of_constants = int(signature[number_of_relations + 1])
#    except IndexError:
#        return # no constants in signature
#    except ValueError:
#        raise SignatureError(
#        "the first line after the relations should contain an integer"
#        + " with the number of constants in the signature file")
#    
#    for index in range(number_of_relations + 2, number_of_relations + number_of_constants + 2):
#        try:
#            line = signature[index]
#            line = line.split(";", 1)[0]  # strip comments
#            constants_set.add(line.rstrip().lower())
#        except IndexError:
#            raise SignatureError("wrong formatting")
#    get_constants_set() # add these new constants to the set, and build the regexp

# This is the function to be called from main
def parse(tokens):
    next_token = tokens.next()
    if next_token != '(':
        raise SyntaxError(lineNumber, next_token, '(')
    
    syntax_tree = parse_so_wff(tokens)
    
    next_token = get_excess_token(tokens)
    if (next_token != None):
        raise TokenExcessError(lineNumber, next_token)

    syntax_tree.check_consistency()

    # check if syntax_tree has any free variables, if so return error
    return syntax_tree

def parse_so_wff(tokens):
    # The leading '(' has already been swallowed
    next_token = tokens.next()
    if next_token in so_wff:
        # Production so_wff --> (so-exists|so-forall)
        quantifier_type = Operator(next_token)

        next_token = tokens.next()
        if next_token != '(':
            raise SyntaxError(lineNumber, next_token, '(')
        
        next_token = tokens.next()
        list_rel = parse_list_rel(tokens, next_token)

        next_token = tokens.next()
        if next_token != '(':	
            raise SyntaxError(lineNumber, next_token, '(')
        
        so_wff_child = parse_so_wff(tokens)

        next_token = tokens.next()
        if next_token != ')':	
            raise SyntaxError(lineNumber, next_token, ')')
        
        return SoWff([quantifier_type, list_rel,\
                so_wff_child])
    else:
        # Production so_wff --> fo_wff
        fo_wff = parse_fo_wff(tokens, next_token)

        #?Checking for correct closing syntax incomplete
        """try:
            next_token = tokens.next()
            if next_token != ')':
                raise SyntaxError(lineNumber, next_token, ')')
        except StopIteration:
            raise SyntaxError(lineNumber, '<END OF LINE>', ')')
        """
        return SoWff([fo_wff])

def parse_fo_wff(tokens, next_token):
    # The leading '(' has already been swallowed
    if next_token in fo_wff:
        qtype = next_token

        # Production fo_wff --> (exists|forall)
        quantifier_type = Operator(qtype)

        # Next token must be '('
        next_token = tokens.next()
        if next_token != '(':
            raise SyntaxError(lineNumber, next_token, '(')
        
        next_token = tokens.next()
        list_var = parse_list_var(tokens, next_token)

        # After parsing the list of variables, next token
        # must be '(' again
        next_token = tokens.next()
        if next_token != '(':
            raise SyntaxError(lineNumber, next_token, '(')

        next_token = tokens.next()
        fo_wff_child = parse_fo_wff(tokens, next_token)

        next_token = tokens.next()
        if next_token != ')':
            msg = "quantifier %s is not being closed properly." %(qtype)
            raise SyntaxError(lineNumber, next_token, ')', msg)
        
        return FoWff([quantifier_type, list_var, fo_wff_child])
    elif next_token in nary_operators:
        if next_token == implies_keyword:
            # Production fo-wff --> (implies)
            # Parse antecedent
            next_token = tokens.next()
            if next_token != '(':
                raise SyntaxError(lineNumber, next_token, '(')
            antecedent = parse_fo_wff(tokens, tokens.next())

            # Parse consequent
            next_token = tokens.next()

            if next_token != '(':
                msg = "missing consequent of 'implies' construct."
                raise SyntaxError(lineNumber, next_token, '(', msg)
            consequent = parse_fo_wff(tokens, tokens.next())

            # Check that the operator closes properly
            next_token = tokens.next()
            if next_token != ')':
                msg = "operator 'implies' is not being closed properly."
                raise SyntaxError(lineNumber, next_token, ')', msg)  

            or_node = Operator(or_keyword)
            not_node = Operator(not_keyword)

            child_node = ListFoWff([FoWff([not_node, antecedent]), \
                    ListFoWff([consequent])])

            return FoWff([or_node, child_node])
        else:
            # Production fo-wff --> (and|or)
            operator_type = Operator(next_token)

            # Next token must be '('
            next_token = tokens.next() 
            if next_token != '(':
                raise SyntaxError(lineNumber, next_token, '(')

            fo_wff_child = parse_fo_wff(tokens, tokens.next())

            # Next token must be '(', unless it's an unary and/or
            next_token = tokens.next() 

            if next_token == ')': # handles unary cases
                return fo_wff_child
            elif next_token != '(':
                raise SyntaxError(lineNumber, next_token, '(')

            fo_wff_list = parse_list_fo_wff(tokens)

            return FoWff([operator_type, fo_wff_child, fo_wff_list])
    elif next_token in unary_operators:
        # Production fo-wff --> (not)
        operator_type = Operator(next_token)

        # Next token must be '('
        next_token = tokens.next()
        if next_token != '(':
            raise SyntaxError(lineNumber, next_token,'(')

        # After the unary relation comes one fo-wff
        fo_wff_child = parse_fo_wff(tokens, tokens.next())
        
        # Check that the operator closes properly
        next_token = tokens.next()
        if next_token != ')':
            raise SyntaxError(lineNumber, next_token, ')')
        
        return FoWff([operator_type, fo_wff_child])
    else:
        # Production fo-wff --> atom
        atom = parse_atom(tokens, next_token)
        return FoWff([atom])

def parse_list_fo_wff(tokens):
    # There is another fo_wff to parse in the current list
    next_fo_wff = parse_fo_wff(tokens, tokens.next())

    next_token = tokens.next()
    if next_token == '(':
        return ListFoWff([next_fo_wff, parse_list_fo_wff(tokens)])
    elif next_token == ')':
        return ListFoWff([next_fo_wff])
    else:
        raise SyntaxError(lineNumber, next_token, ')')

def parse_atom(tokens, next_token):
    # The leading '(' has already been swallowed
    # next_token holds the value of looked-ahead token
    if not relations.match(next_token):
        raise SyntaxError(lineNumber, next_token, '<REL>')

    if not symbols.has_key(next_token):
        if all_symbols.has_key(next_token):
            symbols[next_token] = all_symbols[next_token]
        else:
            raise DefinitionError(lineNumber, \
                    "undefined relation '%s'" %(next_token))

    terms_left = symbols[next_token][0] # arity of the relation

    rel = Rel(next_token)     #this might be a function or a relation
    list_terms = parse_list_term(tokens, tokens.next(), terms_left)

    return Atom([rel, list_terms])

def parse_list_rel(tokens, next_token):
    # There is at least one relation to parse in the current list
    next_rel = parse_rel(next_token, tokens.next())
    
    next_token = tokens.next()
    if next_token != ')':
        # There's another relation in the list
        # Production list_rel --> <REL> <int> list_rel
        next_rel.append(parse_list_rel(tokens, next_token))
        return ListRel(next_rel)
    else:
        # The list is closed
        # Production list_rel --> <REL> <int>
        return ListRel(next_rel)

#This function also parse functions.
def parse_rel(relation, arity):
    # This checks the syntax of the relation-arity tuple
    if not relations.match(relation):
        raise SyntaxError(lineNumber, relation, '<REL>')

    if not (integers.match(arity) or arity == 'inj' or arity == 'func'):
        raise SyntaxError(lineNumber, arity, "<int>/<func>/<inj>")

    if symbols.has_key(relation):
        raise DefinitionError(lineNumber, "relation '%s' already defined" %(relation))
            
    #TODO clean up
    if arity != 'func' and arity != 'inj':
        arity = int(arity)
        if arity <= 0:
            raise DefinitionError(lineNumber, "relation '%s' has nonpositive arity" %(relation))
    else:
        if arity == 'inj':
            symbols[relation] = (2, 1)
            inj_symbols.add(relation)
        else:
            symbols[relation] = (2, 2)
            func_symbols.add(relation)

    if arity == 'func' or arity == 'inj':
        quantified_relations[relation] = arity
        return [Func(relation), Int(2)]
    else:
        quantified_relations[relation] = arity
        symbols[relation] = (arity, 0)
        return [Rel(relation), Int(arity)]

def parse_list_term(tokens, next_token, terms_left):
    # debug: implementing support for constants
    # print constants_set
    if variables.match(next_token):
        term = Var(next_token)
    elif constants.match(next_token):
        term = Const(next_token)
    else:
        raise SyntaxError(lineNumber, next_token, '<VAR>|<CONST>')

    # The recursive call should be made with one term less left to parse
    # for this atom
    terms_left -= 1
    prev_token = next_token # Current token retained for error handling
    next_token = tokens.next()

    if next_token != ')':
        # More terms must be parsed
        if terms_left == 0:
            raise ArityError(lineNumber, terms_left, prev_token)

        return ListTerm([term, parse_list_term(tokens, next_token, terms_left)])
    else:
        # No terms left to parse
        if terms_left > 0:
            raise ArityError(lineNumber, terms_left, prev_token)

        return ListTerm([term])

def parse_list_var(tokens, next_token):
    # There is at least one variable to parse in the current list
    if not variables.match(next_token):
        raise SyntaxError(lineNumber, next_token, '<VAR>')
    
    next_var = [Var(next_token)]

    next_token = tokens.next()
    if next_token != ')':
        # There's another variable in the list
        # Production list_rel --> <REL> <int> list_rel
        next_var.append(parse_list_var(tokens, next_token))
        return ListVar(next_var)
    else:
        # The list is closed
        # Production list_rel --> <REL> <int>
        return ListVar(next_var)

def show_symbol_table():
    print symbols

