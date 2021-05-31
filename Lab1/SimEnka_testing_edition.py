import sys

def get_epsilon_output(state, transitions, visited):
    output = []
    if '$' in transitions[state]:
        for transition_state in transitions[state]['$']:
            output.append(transition_state)
        for transition_state in output:
            if transition_state not in visited:
                visited.append(transition_state)
                output_recursion = get_epsilon_output(transition_state, transitions, visited)
                for temp in output_recursion:
                    if temp not in output:
                        output.append(temp)
        output.append(state)
        return output
    else:
        return []

def get_output(niz, start, transitions):
    current_state = []
    current_state.append(start)
    epsilon_operator_states = get_epsilon_output(start, transitions, [])
    for state in epsilon_operator_states:
        current_state.sort()
        if state not in current_state:
            current_state.append(state)
    string_builder = ''
    string_builder = string_builder + ','.join(current_state)
    for symbol in niz.split(','):
        new_state = []
        for state in current_state:
            if symbol in transitions[state]:
                for transition_state in transitions[state][symbol]:
                    if transition_state not in new_state:
                        new_state.append(transition_state)
        temp_states = []
        for state in new_state:
            epsilon_operator_states = get_epsilon_output(state, transitions, [])
            if epsilon_operator_states:
               for transition_state in epsilon_operator_states:
                   if transition_state not in new_state:
                        temp_states.append(transition_state)
        for state in temp_states:
            if state not in new_state:
                new_state.append(state)
        if new_state:
            current_state = new_state.copy()
            current_state.sort()
            string_builder = string_builder + '|'
            string_builder = string_builder + ','.join(current_state)
        else:
            current_state = new_state.copy()
            string_builder = string_builder + '|'
            string_builder = string_builder + '#'

    return string_builder

def main(input):
    l = []
    a = open(input, 'r')
    l = a.readlines()
    input_line = l[0].strip().split('|')
    states = l[1].strip().split(',')
    symbols = l[2].strip().split(',')
    acceptable_states = l[3].strip().split(',')
    start = l[4].strip()
    temp = []
    for i in range(len(l[5:])):
        temp.append(l[i + 5].strip())
    transitions = {}

    for i in range(len(states)):
        transitions[states[i]] = {}

    for i in range(len(temp)):
        temp1 = temp[i].split('->')
        temp2a = temp1[0].split(',')
        temp2b = temp1[1].split(',')
        transitions[temp2a[0]][temp2a[1]] = []
        if '#' not in temp2b:
            for t in temp2b:
                transitions[temp2a[0]][temp2a[1]].append(t)
    a = ""
    for niz in input_line:
        izlazni_niz = get_output(niz, start, transitions)
        a = a + izlazni_niz + '\n'
    return a
