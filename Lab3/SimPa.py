import sys

def string_assemble(symbol, stack):
    if stack:
        new_stack = stack.copy()
        new_stack.reverse()
        return symbol + '#' + ''.join(new_stack)
    else:
        return symbol + '#$'

def pushStack(stack, word):
    for i in range(len(word)-1, -1, -1):
        stack.append(word[i])

def get_epsilon_output(state, transitions, visited, stack):
    output = []
    if '$' in transitions[state]:
        for i in range(len(transitions[state]['$'])):
            if transitions[state]['$'][i][2] == stack[-1]:
                new_stack = stack.copy()
                new_stack.pop()
                new_stack.append(transitions[state]['$'][i][1])
                output.append([transitions[state]['$'][i][0], i])
                epsilon_recursion = get_epsilon_output(transitions[state]['$'][i][0], transitions, visited, new_stack)
                if epsilon_recursion:
                    for element in epsilon_recursion:
                        output.append([element, i])
    return output


def check_transition(current_state, transitions, stack, string_builder, transition):
    if transition in transitions[current_state]:
        stack_top = stack.pop()
        failed = True
        for trans in transitions[current_state][transition]:
            if trans[2] == stack_top:
                if trans[1] != '$':
                    pushStack(stack, trans[1])
                current_state = trans[0]
                string_builder += '|' + string_assemble(current_state, stack)
                failed = False
        if failed:
            failed_again = True
            if '$' in transitions[current_state]:
                for trans in transitions[current_state]['$']:
                    if trans[2] == stack_top:
                        if trans[1] != '$':
                            pushStack(stack, trans[1])
                        current_state = trans[0]
                        string_builder += '|' + string_assemble(current_state, stack)
                        failed_again = False
            if failed_again:
                string_builder += '|fail'
                stack.append(stack_top)
                return current_state, string_builder
            else:
                if len(stack) > 0:
                    current_state, string_builder = check_transition(current_state, transitions, stack, string_builder,
                                                                     transition)
                else:
                    string_builder += '|fail'
                    return current_state, string_builder

        return current_state, string_builder
    else:
        stack_top = stack.pop()
        failed_again = True
        if '$' in transitions[current_state]:
            for trans in transitions[current_state]['$']:
                if trans[2] == stack_top:
                    if trans[1] != '$':
                        pushStack(stack, trans[1])
                    current_state = trans[0]
                    string_builder += '|' + string_assemble(current_state, stack)
                    failed_again = False
        if failed_again:
            string_builder += '|fail'
            stack.append(stack_top)
            return current_state, string_builder
        else:
            if len(stack) > 0:
                current_state, string_builder = check_transition(current_state, transitions, stack, string_builder,
                                                             transition)
            else:
                string_builder += '|fail'
                return current_state, string_builder
        return current_state, string_builder


def get_output(niz, start, transitions, stack_start, acceptable_states):
    current_state = start
    stack = [stack_start]
    string_builder = ''

    for transition in niz.split(','):
        if len(stack) > 0:
            current_state, string_builder = check_transition(current_state, transitions, stack, string_builder,
                                                             transition)
        else:
            string_builder += '|fail'
        if string_builder.endswith('fail'):
            break
            stack = []

    while len(stack) > 0 and not string_builder.endswith('fail') and current_state not in acceptable_states:
        if '$' in transitions[current_state]:
            current_state, string_builder = check_transition(current_state, transitions, stack, string_builder, '$')
        else:
            break
        if string_builder.endswith('fail'):
            string_builder = string_builder[:-5]
            break

    if current_state in acceptable_states and not string_builder.endswith('fail'):
        string_builder += '|1'
    else:
        string_builder += '|0'
    return string_builder

def main():
    l = []
    for line in sys.stdin:
        l.append(line)

    input_line = l[0].strip().split('|')
    states = l[1].strip().split(',')
    symbols = l[2].strip().split(',')
    stack_symbols = l[3].strip().split(',')
    acceptable_states = l[4].strip().split(',')
    start = l[5].strip()
    stack_start = l[6].strip()
    temp = []
    for i in range(len(l[7:])):
        temp.append(l[i + 7].strip())
    transitions = {}

    for i in range(len(states)):
        transitions[states[i]] = {}

    for i in range(len(temp)):
        temp1 = temp[i].split('->')
        temp2a = temp1[0].split(',')
        temp2b = temp1[1].split(',')
        temp2b.append(temp2a[2])
        if temp2a[1] in transitions[temp2a[0]]:
            transitions[temp2a[0]][temp2a[1]].append(temp2b)
        else:
            transitions[temp2a[0]][temp2a[1]] = []
            transitions[temp2a[0]][temp2a[1]].append(temp2b)

    #for i in range (len(l)):
        #print(l[i])

    result = ''

    result += string_assemble(start, [stack_start])

    #print(result)

    for niz in input_line:
        output = get_output(niz, start, transitions, stack_start, acceptable_states)
        print(result + output)


if __name__ == "__main__":
    main()