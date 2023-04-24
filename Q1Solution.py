from Packages.FA.dfa import VisualDFA
from Packages.FA.nfa import VisualNFA
from Packages.utils import read_fa, create_standard_fa
import os


def get_nfa(jsonpath:"str") -> "VisualNFA":
    
    read_fa(jsonpath)
    fa = create_standard_fa(1)
    nfa = VisualNFA(fa)

    return nfa


def lambda_transition(states: list["str"], nfa: "VisualNFA"):
  stack = list(states)
  res = set(states)
  while len(stack):
    state = stack.pop(0)
    if (tr := nfa.transitions.get(state).get("")):
      for st in tr:
        res.add(st)
        stack.append(st)
  
  return frozenset(res)
      

def ordinary_transition(symbol: "str", states: list["str"], nfa: "VisualNFA"):
  res = set()
  stack = list(states)

  while len(stack):
    state = stack.pop(0)
    if (tr := nfa.transitions.get(state).get(symbol)):
      for target in tr:
        target = lambda_transition([target], nfa)
        res.update(target)
      
  return frozenset(res)


def nfa_to_dfa(nfa:"VisualNFA") -> "dict":

  result = {
    "states": set(),
    "input_symbols": set(nfa.input_symbols),
    "transitions": dict(),
    "initial_state": set(),
    "final_states": set()
  }
  
  initial_state = frozenset(lambda_transition([nfa.initial_state], nfa))
  queue = [initial_state]

  result["states"].add(initial_state)
  result["initial_state"] = initial_state

  while len(queue):
    states = queue.pop()
    for symbol in nfa.input_symbols:
      targets = ordinary_transition(symbol, states, nfa)
      
      if (not result["transitions"].get(states)):
        result["transitions"][states] = dict()

      if len(targets):
        result["transitions"][states][symbol] = "".join(targets)
        if (targets not in queue and targets not in result["states"]):
          queue.insert(0, targets)

        result["states"].add(targets)

      else:
        result["transitions"][states][symbol] = "TRAP"
        if "TRAP" not in result["states"]:
          result["states"].add("TRAP")
          result["transitions"]["TRAP"] = {key: "TRAP" for key in result["input_symbols"]}

  for state in result["states"]:
    for final_state in nfa.final_states:
      if final_state in state:
        result["final_states"].add(state)

  return result


path = input("Enter the NFA json file directory:\n")

if not os.path.isfile(path):
  raise FileNotFoundError(f"The directory {path} you provided is invalid.")

nfa = get_nfa(path)

res = nfa_to_dfa(nfa)


res["states"] = str(set(map(lambda fr: "".join(fr), res["states"])))
res['input_symbols'] = str(res['input_symbols'])
res['final_states'] = str(set(map(lambda fr: "".join(fr), res["final_states"])))

res["initial_state"] = "".join(res["initial_state"])



new_transition_dict = dict()
for key, value in res["transitions"].items():
  new_transition_dict["".join(key)] = value
  
res["transitions"] = new_transition_dict

import json

with open("NFA.json", "w+") as f:
  json.dump(res, f, indent=4)
