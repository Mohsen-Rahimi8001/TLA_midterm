import json


dfa = dict()


def InputFile(fileName):
    global dfa
    with open(fileName) as file:
        dfa = json.load(file)
    file.close()



def OutputFile():
    global dfa
    with open('SDFA.json', 'w') as file:
        json.dump(dfa, file)
    file.close()



def RemoveUnreachableStates():
    pass



def MergeEquivalentStates():
    pass




def main():
    # enter the dfa.json file name
    fileName = input("File Name: ")
    fileName = fileName.strip() + '.json' if fileName[-5:] != '.json' else fileName.strip()

    # give input DFA.json file 
    InputFile(fileName)

    # Remove Unreachable States
    RemoveUnreachableStates()
    
    # Merge Equivalent States
    MergeEquivalentStates()

    # get back SDFA.json file
    OutputFile()