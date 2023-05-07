import json


def InputFile(fileName):
    with open(fileName) as file:
        return json.load(file)


def OutputFile(dfa):
    with open('SDFA.json', 'w') as file:
        json.dump(dfa, file, indent=4)
    file.close()


def minimize_dfa(input_dict):
    # Replace single quotes with double quotes in states and input_symbols
    input_dict['states'] = [string.replace("'", "\"") for string in input_dict['states']]
    input_dict['input_symbols'] = [string.replace("'", "\"") for string in input_dict['input_symbols']]
 
    # Parse the states and input_symbols as sets
    input_dict['states'] = set(input_dict['states'])
    input_dict['input_symbols'] = set(input_dict['input_symbols'])
   
    # Initialize variables
    partitions = []
    final_states = set(input_dict['final_states'])
    non_final_states = set(input_dict['states'] - final_states)

    partitions.append(final_states)
    partitions.append(non_final_states)
    new_partitions = []

    # Iteratively refine the partitions
    while True:
        new_partitions = partitions.copy()
        for partition in partitions:
            for symbol in input_dict['input_symbols']:
                # Group states based on where they transition to on the given symbol
                groups = {}
                for state in partition:
                    target_state = input_dict['transitions'][state][symbol]
                    if target_state in groups:
                        groups[target_state].add(state)
                    else:
                        groups[target_state] = {state}

                # Add groups to the new partitions
                if len(groups) > 1:
                    if partition in new_partitions:
                        new_partitions.remove(partition)
                    print(f"group->{groups} val->{groups.values()}")
                    for group in groups.values():
                        new_partitions.append(group)
            print(f"in for ---> partotin: {new_partitions}")
        print(f"Partitions: {partitions}, new Partitions: {new_partitions}\n")

        if partitions == new_partitions:
            break
        else:
            partitions = new_partitions


    print(f"=========Partitions: {partitions}, new Partitions: {new_partitions}=========")
    # Generate the minimized DFA
    new_states = {}
    new_final_states = set()
    for i, partition in enumerate(new_partitions):
        state_name = "q" + str(i)
        new_states[state_name] = {}
        for symbol in input_dict['input_symbols']:
            target_state = input_dict['transitions'][list(partition)[0]][symbol]
            for p in partitions:
                if target_state in p:
                    new_target_state = "q" + str(list(partitions).index(p))
                    break
            new_states[state_name][symbol] = new_target_state

        if len(partition & final_states) > 0:
            new_final_states.add(state_name)

    min_dfa = {
        'states': set(new_states.keys()),
        'input_symbols': input_dict['input_symbols'],
        'transitions': new_states,
        'initial_state': 'q0',
        'final_states': list(new_final_states)
    }

    return min_dfa



# Example usage
input_json = '''
{
    "states": ["q0","q1","q2","q3","q4"],
    "input_symbols": ["0","1"],
    "transitions": {
        "q0": {
            "0": "q1",
            "1": "q3"
        },
        "q1": {
            "0": "q2",
            "1": "q4"
        },
        "q2": {
            "0": "q1",
            "1": "q4"
        },
        "q3": {
            "0": "q2",
            "1": "q4"
        },
        "q4": {
            "0": "q4",
            "1": "q4"
        }
    },
    "initial_state": "q0",
    "final_states": ["q4"]
}   '''


# Parse the input JSON string
dfa = json.loads(input_json)

# Minimize the DFA
min_dfa = minimize_dfa(dfa)

# Print the minimized DFA as JSON
print(f"\n\n{min_dfa}")
# print(json.dumps(min_dfa, indent=4))


# def main():
#     # enter the dfa.json file name
#     fileName = input("File Name: ")
#     fileName = fileName.strip() + '.json' if fileName[-5:] != '.json' else fileName.strip()

#     # give input DFA.json file 
#     dfa = InputFile(fileName)

#     # Minimize the DFA
#     min_dfa = minimize_dfa(dfa) 

#     # get back SDFA.json file
#     OutputFile(min_dfa)
# main()