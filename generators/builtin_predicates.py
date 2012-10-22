def name(x, n):
    if x == 1:
        return " zero"
    elif x == n:
        return " max"
    else:
        return " obj" + str(x-1)

def generate_obj(n):
    s = []
    for i in range(1, n-1):
        s.append("obj" + str(i))
    return s

def generate_nocycles(n):
    s = []
    for i in range(1, n+1):
        s.append("(not_e" + name(i, n) + name(i, n) + ")")
    return s 

## tested!
def generate_suc(n):
    if n < 2:
        raise ValueError
    if n == 2:
        return ["(suc zero max)"]

    s = ["(suc zero obj1)"]
    for i in range(1, n-2):
        s.append("(suc obj" + str(i) + " obj" + str(i+1) + ")")
    s.append("(suc obj" + str(n-2) + " max)")
    return s

def generate_lt(n):
    return generate_ascending_2arity('lt',n)

## tested! (against (n**2-n)/2)
def generate_ascending_2arity(rel,n):
    if n < 2:
        raise ValueError
    if n == 2:
        return ["(" + rel + " zero max)"]
    s = []

    # zero < obj_i
    # zero < max
    for i in range(1, n-1):
        s.append("(" + rel + " zero obj" + str(i) + ")")
    s.append("(" + rel + " zero max)")

    # obj_i < obj_j
    for i in range(1, n-1):
        for j in range(i+1, n-1):
            s.append("(" + rel + " obj" + str(i) + " obj" + str(j) + ")")

    # obj_i < max
    for i in range(1, n-1):
        s.append("(" + rel + " obj" + str(i) + " max)")

    return s

# tested!
def generate_descending_2arity(rel,n):
    s = generate_lt(n)
    new_s = []
    for p in s:
        pred = p.replace('(', ' ( ').replace(')', ' ) ').split()
        new_s.append("(" + rel + " " + " ".join([pred[3], pred[2]]) + ")")
    return new_s
    
def generate_gt(n):
    return generate_descending_2arity('gt',n)
    
def generate_all_2arity(rel,n):
    if n < 2:
        raise ValueError
    if n == 2:
        return ["(" + rel + " zero max)","(" + rel + " zero zero)",\
                "(" + rel + " max zero)","(" + rel + " max max)"]
    s = []

    # zero < obj_i
    # zero < max
    s.append("(" + rel + " zero zero)")
    for i in range(1, n-1):
        s.append("(" + rel + " zero obj" + str(i) + ")")
    s.append("(" + rel + " zero max)")

    # obj_i < obj_j
    for i in range(1, n-1):
        s.append("(" + rel + " obj" + str(i) + " zero)")
        for j in range(1, n-1):
            s.append("(" + rel + " obj" + str(i) + " obj" + str(j) + ")")
        s.append("(" + rel + " obj" + str(i) + " max)")

    # obj_i < max
    s.append("(" + rel + " max zero)")
    for i in range(1, n-1):
        s.append("(" + rel + " max obj" + str(i) + ")")
    s.append("(" + rel + " max max)")
    
    return s
    
def generate_free_rel_2arity(n, relName):
    return generate_all_2arity("not_" + relName,n)

def generate_free_rel_1arity(n, relName):
    return generate_all_1arity("not_" + relName,n)

def generate_all_1arity(rel,n):
    s = []
    s.append("(" + rel + " zero)")

    for i in range(1, n-1):
        s.append("(" + rel + " obj" + str(i) +")")
        
    s.append("(" + rel + " max)")
    
    return s
    
def generate_free_domain(n, funcName):
    return generate_all_1arity("free_domain_" + funcName,n)
    
def generate_free_range(n, funcName):
    return generate_all_1arity("free_range_" + funcName,n)
    
def generate_suc_forall(a_vars,maxim):
    s = []
    last = "zero"
    so_forall_vars = []
    for i in range (0, len(a_vars)-1):
        if (abs(a_vars[i+1]) == 0):
            break
        var1 = abs(a_vars[i])
        print var1
        if var1 == 1:
            var1 = "zero"
        elif var1 == maxim:
            var1 = "max"
        else:
            var1 = "obj" + str(var1 - 1)
        
        so_forall_vars += [var1]
            
        var2 = abs(a_vars[i+1])
        if var2 == 1:
            var2 = "zero"
        elif var2 == maxim:
            var2 = "max"
        else:
            var2 = "obj" + str(var2 - 1)
            
        last = var2
        s.append("(so-forall_suc_t " + var1 + " " + var2 + ")")
        
    #(not_e) forall var
    #t is forall relation
    so_forall_vars += [last]
    s.append("(so-forall_zero_t " + so_forall_vars[0] + ")")
    s.append("(so-forall_max_t " + so_forall_vars[-1] + ")")
    return s