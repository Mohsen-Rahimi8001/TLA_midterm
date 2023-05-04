from Packages.FA.dfa import VisualDFA
from Packages.FA.nfa import VisualNFA
from Packages.utils import read_fa, create_standard_fa
import os

def get_fa(jsonpath:'str') -> VisualDFA | VisualNFA:
    try:
        read_fa(jsonpath)
        fa = create_standard_fa()
        dfa = VisualNFA(fa)

        return dfa
    except Exception as e:
        try:
            read_fa(jsonpath)
            fa = create_standard_fa(1)
            nfa = VisualNFA(fa)

            return nfa
        except Exception as e:
            return 0

def star(fa:VisualDFA|VisualNFA) -> dict:

    res = {
    "states": set(fa.states),
    "input_symbols": set(fa.input_symbols),
    "transitions": dict(),
    "initial_state": fa.initial_state,
    "final_states": set(fa.final_states)
    }

    for state, value in fa.transitions.items():
        new_transition = dict()
        for symbol, targetset in value.items():
            new_transition[symbol] = str(set(targetset))
        
        res['transitions'][state] = new_transition

    new_final_state = 'fi'
    res['states'].add(new_final_state)
    res['transitions'][new_final_state] = {
        "": str({fa.initial_state})
    }

    for state in fa.final_states:
        res["transitions"][state][""] = str({new_final_state})

    res['final_states'] = {new_final_state}
    res['transitions'][res['initial_state']][''] = str(set(res['final_states']))
    res["states"] = str(res["states"])
    res["input_symbols"] = str(res["input_symbols"])
    res["initial_state"] = str(res["initial_state"])
    res["final_states"] = str(res["final_states"])

    return res
    

def union(fa1, fa2) -> dict:
    pass

def concatenation(fa1, fa2) -> dict:
    pass


path = os.path.join('.', 'Packages', 'samples', 'phase4-sample', 'star', 'in', 'FA.json')

fa = get_fa(path)
if not fa:
    raise Exception("The json file you provided is neither nfa nor dfa.")

res = star(fa)


import json

with open("RFA.json", "w+") as f:
    json.dump(res, f, indent=4)

