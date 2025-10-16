!pip install graphviz

from graphviz import Digraph
from collections import deque
import copy
import re

# Initial facts
facts = set([
    "American(Robert)",
    "Enemy(A, America)",
    "Owns(A, T1)",       # Existential instantiation of missile owned by A
    "Missile(T1)"
])

rules = [
    (["Missile(x)"], "Weapon(x)"),
    (["Missile(x)", "Owns(A, x)"], "Sells(Robert, x, A)"),
    (["Enemy(x, America)"], "Hostile(x)"),
    (["American(p)", "Weapon(q)", "Sells(p, q, r)", "Hostile(r)"], "Criminal(p)")
]

query = "Criminal(Robert)"

# Utility to extract predicate and arguments
def parse_predicate(fact):
    pred = fact[:fact.find('(')]
    args = fact[fact.find('(')+1:-1].split(', ')
    return pred, args

# Checks if a token is a variable (lowercase letter)
def is_variable(token):
    return token.islower()

# Standardize variables apart by renaming them uniquely per rule application
var_counter = 0
def standardize_apart(premises, conclusion):
    global var_counter
    var_map = {}
   
    def rename_vars(expr):
        pred, args = parse_predicate(expr)
        new_args = []
        for a in args:
            if is_variable(a):
                if a not in var_map:
                    var_map[a] = f"{a}{var_counter}"
                new_args.append(var_map[a])
            else:
                new_args.append(a)
        return f"{pred}({', '.join(new_args)})"
   
    var_counter += 1
    new_premises = [rename_vars(p) for p in premises]
    new_conclusion = rename_vars(conclusion)
    return new_premises, new_conclusion

# Unification algorithm: returns substitution or None if fails
def unify(x, y, subs):
    # If subs is None, unification failed earlier
    if subs is None:
        return None
    if x == y:
        return subs
    if is_variable(x):
        return unify_var(x, y, subs)
    if is_variable(y):
        return unify_var(y, x, subs)
    if '(' in x and '(' in y:
        # Both predicates
        px, argsx = parse_predicate(x)
        py, argsy = parse_predicate(y)
        if px != py or len(argsx) != len(argsy):
            return None
        for a,b in zip(argsx, argsy):
            subs = unify(a,b,subs)
            if subs is None:
                return None
        return subs
    return None

def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    elif x in subs:
        return unify(var, subs[x], subs)
    else:
        # Occurs check (prevent var = f(var))
        if occurs_check(var, x, subs):
            return None
        subs = subs.copy()
        subs[var] = x
        return subs

def occurs_check(var, x, subs):
    if var == x:
        return True
    if is_variable(x) and x in subs:
        return occurs_check(var, subs[x], subs)
    return False

# Apply substitution to expression
def substitute(expr, subs):
    pred, args = parse_predicate(expr)
    new_args = []
    for a in args:
        val = a
        while val in subs:
            val = subs[val]
        new_args.append(val)
    return f"{pred}({', '.join(new_args)})"

# Find substitutions satisfying all premises from known facts
def find_substitutions(premises, known_facts):
    subs_list = [{}]  # Start with empty substitution
    for premise in premises:
        new_subs_list = []
        for fact in known_facts:
            for subs in subs_list:
                unifier = unify(premise, fact, subs)
                if unifier is not None:
                    new_subs_list.append(unifier)
        subs_list = new_subs_list
        if not subs_list:
            return []
    return subs_list

def forward_chaining_with_graph(facts, rules, query):
    inferred = set()
    agenda = deque(facts)
    facts = set(facts)

    g = Digraph('Forward_Chaining')
    g.attr(rankdir='LR', size='10,6')

    for f in facts:
        g.node(f, label=f, color='green', style='filled')

    while agenda:
        fact = agenda.popleft()
        if fact == query:
            return True, g
        if fact in inferred:
            continue
        inferred.add(fact)

        for premises, conclusion in rules:
            std_premises, std_conclusion = standardize_apart(premises, conclusion)
            substitutions = find_substitutions(std_premises, facts)
            for subs in substitutions:
                concl_inst = substitute(std_conclusion, subs)
                if concl_inst not in facts:
                    facts.add(concl_inst)
                    agenda.append(concl_inst)
                    g.node(concl_inst, label=concl_inst, color='yellow', style='filled')
                    for premise in std_premises:
                        prem_inst = substitute(premise, subs)
                        g.edge(prem_inst, concl_inst, color='blue')

    return query in facts, g

proved, graph = forward_chaining_with_graph(facts, rules, query)

if proved:
    print(f"Query '{query}' is proved from the knowledge base.")
else:
    print(f"Query '{query}' cannot be proved from the knowledge base.")

graph.render('forward_chaining_output', format='png', cleanup=True)

from IPython.display import Image
Image('forward_chaining_output.png')