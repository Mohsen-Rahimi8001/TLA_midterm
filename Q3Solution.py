from Packages.FA.dfa import VisualDFA
from Packages.FA.nfa import VisualNFA
from Packages.utils import read_fa, create_standard_fa
import os

def get_dfa(jsonpath: "str") -> "VisualDFA":
    try:
        read_fa(jsonpath)
        fa = create_standard_fa()
        dfa = VisualNFA(fa)

        return dfa
    except Exception as e:
        return 0

def get_nfa(jsonpath:"str") -> "VisualNFA":
    try:
        read_fa(jsonpath)
        fa = create_standard_fa(1)
        nfa = VisualNFA(fa)

        return nfa
    except Exception as e:
        return 0

def check_for_nfa(nfa: "VisualNFA", string: "str") -> bool:
    state = nfa.initial_state
    check_paths = [(state, 0)]
    while (len(check_paths)):
        path = check_paths.pop(0)
        state = path[0]
        flag = True
        for i in range(path[1], len(string)):
            char = string[i]
            
            lambda_tr = nfa.transitions.get(state).get("")
            
            if lambda_tr:
                for target in lambda_tr:
                    check_paths.append((target, i))
            
            new_states = nfa.transitions.get(state).get(char)
            
            if not new_states:
                flag = False
                break
            
            else:
                new_states = list(new_states)
                state = new_states.pop(0)
                for st in new_states:
                    check_paths.append((st, i + 1))

        if flag and state in nfa.final_states:
            return True
    
    return False


def check_for_dfa(dfa: "VisualDFA", string: "str") -> bool:
    state = dfa.initial_state
    for char in string:
        state = dfa.transitions.get(state).get(char)
        if not state:
            return False
    
    if state in dfa.final_states:
        return True
    
    return False

path = input("Enter the FA json file path: ")

if not (os.path.isfile(path)):
    raise FileNotFoundError(f"The file {path} you provided does not exist.")

if (dfa := get_dfa(path)):
    string = input(f"\nThe alphabet is: {set(dfa.input_symbols)}.\nEnter arbitrary string to check: ")
    print(check_for_dfa(dfa, wstring))

else:
    nfa = get_nfa(path)

    if not nfa:
        raise ValueError("The jsonfile is neither nfa nor dfa.")

    string = input(f"\nThe alphabet is: {set(nfa.input_symbols)}.\nEnter arbitrary string to check: ")

    print(check_for_nfa(nfa, string))
    