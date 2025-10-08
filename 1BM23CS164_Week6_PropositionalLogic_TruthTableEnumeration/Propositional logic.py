from itertools import product

def implies(p, q):
    return (not p) or q

def evaluate(sentence, assignment):
    """
    Evaluate a sentence given a truth assignment.
    sentence: function that takes assignment dict and returns bool
    assignment: dict of variable->bool
    """
    return sentence(assignment)

def truth_table_enumeration(kb, query, symbols):
    """
    kb: list of sentences (functions from assignment dict to bool)
    query: sentence (function)
    symbols: list of propositional symbols (strings)
    
    Returns True if KB entails query, False otherwise
    """
    for values in product([True, False], repeat=len(symbols)):
        assignment = dict(zip(symbols, values))
        
        # Check if KB is true in this model
        kb_true = all(evaluate(sentence, assignment) for sentence in kb)
        
        if kb_true:
            # Check if query is true in this model
            if not evaluate(query, assignment):
                return False  # KB true but query false in this model → no entailment
    
    return True  # Query true in all KB models → entailment


# Define sentences as Python functions

# Example KB:
# A -> B
# B -> C
# A

def sentence1(a):  # A -> B
    return implies(a['A'], a['B'])

def sentence2(a):  # B -> C
    return implies(a['B'], a['C'])

def sentence3(a):  # A
    return a['A']

def query(a):      # C
    return a['C']

kb = [sentence1, sentence2, sentence3]
query_sentence = query
symbols = ['A', 'B', 'C']

entails = truth_table_enumeration(kb, query_sentence, symbols)
print(f"Does KB entail the query? {entails}")
