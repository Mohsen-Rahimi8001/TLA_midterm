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
    

def union(fa1:VisualDFA|VisualNFA, fa2:VisualDFA|VisualNFA) -> dict:
    new_init = 'q0'
    new_fi = 'q1'
    
    new_states = set()
    for i in range(len(fa1.states)):
        new_states.add(f"q{i}1")

    for i in range(len(fa2.states)):
        new_states.add(f"q{i}2")
    

    res = {
    "states": new_states,
    "input_symbols": set(fa1.input_symbols).union(fa2.input_symbols),
    "transitions": dict(),
    "final_states": str({new_fi})
    }

    res['states'].add(new_init)
    res['initial_state'] = new_init
    res['transitions'] = {
        new_init: {
            '': str(
                    {
                    fa1.initial_state+"1", fa2.initial_state+"2"
                }
            )
        }
    }

    for state, value in fa1.transitions.items():
        new_transition = dict()
        for symbol, targetset in value.items():
            new_transition[symbol] = set()
            for target in targetset:
                new_transition[symbol].add(target+"1")

            if symbol != "" or state not in fa1.final_states:
                new_transition[symbol] = str(new_transition[symbol])
            else:
                new_transition[symbol] = new_transition[symbol]
        
        res['transitions'][state+"1"] = new_transition

    
    for state, value in fa2.transitions.items():
        new_transition = dict()
        for symbol, targetset in value.items():
            new_transition[symbol] = set()
            for target in targetset:
                new_transition[symbol].add(target+"2")
            
            if symbol != "" or state not in fa2.final_states:
                new_transition[symbol] = str(new_transition[symbol])
            else:
                new_transition[symbol] = new_transition[symbol]

        res['transitions'][state+"2"] = new_transition

    for final in fa1.final_states:
        new_final = final+"1"
        if (res['transitions'].get(new_final)):
            res['transitions'][new_final][""] = str({new_fi})
        else:
            res["transitions"][new_final] = {
                "": str({new_fi})
            }


    for final in fa2.final_states:
        new_final = final+"2"
        if (res['transitions'].get(new_final)):
            res['transitions'][new_final][""] = str({new_fi})
        else:
            res["transitions"][new_final] = {
                "": str({new_fi})
            }
    
    res["states"].add(new_fi)

    res['input_symbols'] = str(res['input_symbols'])
    res['states'] = str(res['states'])

    return res

def concat(fa1:VisualDFA|VisualNFA, fa2:VisualDFA|VisualNFA) -> dict:
    new_fi = 'q1'
    
    new_states = set()
    for i in range(len(fa1.states)):
        new_states.add(f"q{i}1")

    for i in range(len(fa2.states)):
        new_states.add(f"q{i}2")
    
    res = {
    "states": new_states,
    "input_symbols": set(fa1.input_symbols).union(fa2.input_symbols),
    "transitions": dict(),
    "final_states": str({new_fi}),
    "initial_state": fa1.initial_state + "1"
    }

    for state, value in fa1.transitions.items():
        new_transition = dict()
        for symbol, targetset in value.items():
            new_transition[symbol] = set()
            for target in targetset:
                new_transition[symbol].add(target+"1")
            
            if symbol != "" or state not in fa1.final_states:
                new_transition[symbol] = str(new_transition[symbol])
            else:
                new_transition[symbol] = new_transition[symbol]

        res['transitions'][state+"1"] = new_transition

    for state in fa1.final_states:
        state_name = state + "1"

        if res['transitions'][state_name].get(""):
            res["transitions"][state_name][""].add(fa2.initial_state + "2")
        else:
            res["transitions"][state_name][""] = str({fa2.initial_state + "2"})

    for state, value in fa2.transitions.items():
        new_transition = dict()
        for symbol, targetset in value.items():
            new_transition[symbol] = set()
            for target in targetset:
                new_transition[symbol].add(target+"2")
            
            if symbol != "" or state not in fa2.final_states:
                new_transition[symbol] = str(new_transition[symbol])
            else:
                new_transition[symbol] = new_transition[symbol]

        res['transitions'][state+"2"] = new_transition

    for state in fa2.final_states:
        state_name = state + "2"

        if res['transitions'][state_name].get(""):
            res["transitions"][state_name][""].add(new_fi)
        else:
            res["transitions"][state_name][""] = str({new_fi})

    res["states"].add(new_fi)

    res['input_symbols'] = str(res['input_symbols'])
    res['states'] = str(res['states'])

    return res

operation = input("Enter the operation you want to perform:(star, concat, union) ")

if operation.lower() in ["concat", "union"]:

    path1 = input("Enter the first fa file path: ")
    if not os.path.isfile(path1):
        raise FileNotFoundError(f"the path {path1} you provided is invalid.")

    path2 = input("Enter the second fa file path: ")
    if not os.path.isfile(path2):
        raise FileNotFoundError(f"the path {path2} you provided is invalid.")

    fa1 = get_fa(path1)
    fa2 = get_fa(path2)
    if not fa1 or not fa2:
        raise Exception("Json files you provided are neither nfa nor dfa.")

    res = concat(fa1, fa2) if operation.lower() == 'concat' else union(fa1, fa2)

elif operation.lower() == "star":

    path1 = input("Enter the first fa file path: ")
    if not os.path.isfile(path1):
        raise FileNotFoundError(f"the path {path1} you provided is invalid.")

    fa1 = get_fa(path1)
    if not fa1:
        raise Exception("the json file you provided is neither nfa nor dfa.")

    res = star(fa1)


import json

with open("RFA.json", "w+") as f:
    json.dump(res, f, indent=4)

