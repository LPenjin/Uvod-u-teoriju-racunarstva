import sys


def bfs(state, table, i, j):
    combined = [state[i], state[j]]
    queue = [[i, j]]
    table[i][j] = 3
    while queue:
        new_queue = []
        for next in queue:
            for row in range(len(table)):
                if row != next[0] and table[row][next[1]] == 2:
                    table[row][next[1]] = 3
                    new_queue.append([row, next[1]])
                    if state[row] not in combined:
                        combined.append(state[row])
            for column in range(len(table)):
                if column != next[1] and table[next[0]][column] == 2:
                    table[next[0]][column] = 3
                    new_queue.append([next[0], column])
                    if state[column] not in combined:
                        combined.append(state[column])

        queue = new_queue.copy()
    return combined


def findUnreachable(transitions, start):
    bio = [start]
    queue = [start]
    while queue:
        new_queue = []
        for element in queue:
            for key in transitions[element].keys():
                if transitions[element][key][0] not in bio:
                    new_queue.append(transitions[element][key][0])
                    bio.append(transitions[element][key][0])
        queue = new_queue.copy()
    return bio


def minimize(transitions, table, acceptable_states, states):
    marked = 1
    maybe_acceptable = 2
    for i in range(len(table)):
        for j in range(i):
            if states[i] in acceptable_states and states[j] not in acceptable_states \
                    or states[i] not in acceptable_states and states[j] in acceptable_states:
                table[i][j] = marked
            else:
                table[i][j] = maybe_acceptable

    perm = True
    while perm:
        perm = False
        for i in range(len(table)):
            for j in range(i):
                if table[i][j] == maybe_acceptable:
                    for key in transitions[states[i]].keys():
                        tablei = states.index(transitions[states[i]][key][0])
                        tablej = states.index(transitions[states[j]][key][0])
                        if table[tablei][tablej] == marked or table[tablej][tablei] == marked:
                            table[i][j] = marked

    combinations = []
    for i in range(len(table)):
        for j in range(i):
            if table[i][j] == maybe_acceptable:
                combinations.append(bfs(states, table, i, j))

    return combinations


def main():
    l = []
    for line in sys.stdin:
        l.append(line)

    states = l[0].strip().split(',')
    symbols = l[1].strip().split(',')
    acceptable_states = l[2].strip().split(',')
    start = l[3].strip()
    temp = []

    for i in range(len(l[4:])):
        temp.append(l[i + 4].strip())
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

    reachable_states = findUnreachable(transitions, start)
    new_states = []
    for state in states:
        if state not in reachable_states:
            del (transitions[state])
            if state in acceptable_states:
                del (acceptable_states[acceptable_states.index(state)])
        else:
            new_states.append(state)

    states = new_states.copy()
    table = [[0 for i in range(len(states))] for j in range(len(states))]
    combinations = minimize(transitions, table, acceptable_states, states)
    for combination in combinations:
        combination.sort()
        if start in combination and start != combination[0]:
            start = combination[0]
        for element in combination[1:]:
            del(states[states.index(element)])
            if element in acceptable_states:
                del(acceptable_states[acceptable_states.index(element)])
            for transition in transitions.keys():
                for key in transitions[transition].keys():
                    if transitions[transition][key][0] == element:
                        transitions[transition][key][0] = combination[0]
            del(transitions[element])
    print(','.join(states))
    print(','.join(symbols))
    print(','.join(acceptable_states))
    print(start)
    for element in transitions.keys():
        for key in transitions[element].keys():
            print(str(element) + ',' + str(key) + '->' + str(transitions[element][key][0]))


main()
