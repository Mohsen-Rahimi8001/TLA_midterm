import json


EPSILON = ''

def FA2RegEx(dfa):
    # Initialize the equation system for each state pair.
    n = len(dfa['states'])
    A = [[EPSILON if i == j else '' for j in range(n)] for i in range(n)]
    for state, transitions in dfa['transitions'].items():
        i = dfa['states'].index(state)
        for symbol, dest in transitions.items():
            j = dfa['states'].index(dest)
            if A[i][j]:
                A[i][j] += '+' + symbol
            else:
                A[i][j] = symbol

    # Solve the equation system using Arden's lemma.
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if A[i][k] and A[k][k] and A[k][j]:
                    s1 = A[i][k]
                    s2 = A[k][k] + '*' + A[k][j]
                    if A[i][j]:
                        A[i][j] += '+' + s1 + s2
                    else:
                        A[i][j] = s1 + s2

    # The resulting regex is the expression from the start state to the accept state.
    start = dfa['start']
    accept = dfa['accept'][0]
    regex = A[dfa['states'].index(start)][dfa['states'].index(accept)]
    return regex


def json_to_regex(json_data):
    print(json_data)
    data = json.loads(json_data)
    return FA2RegEx(data)


def InputFile(fileName):
    with open(fileName) as file:
        json_to_regex(json.load(file))
    file.close()


# enter the dfa.json file name
fileName = input("File Name: ")
fileName = fileName.strip() + '.json' if fileName[-5:] != '.json' else fileName.strip()

# give input DFA.json file 
InputFile(fileName)