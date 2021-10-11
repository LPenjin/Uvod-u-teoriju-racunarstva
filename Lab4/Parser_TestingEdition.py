def process_S():
    global string_builder
    global pointer
    string_builder += 'S'
    if len(input) == 0 or pointer >= len(input):
        return False
    elif input[pointer] == 'a':
        pointer += 1
        return (proccess_A() and proccess_B())
    elif input[pointer] == 'b':
        pointer += 1
        return (proccess_B() and proccess_A())
    else:
        return False


def proccess_A():
    global string_builder
    global pointer
    string_builder += 'A'
    if len(input) == 0 or pointer >= len(input):
        return False
    elif input[pointer] == 'b':
        pointer += 1
        return proccess_C()
    elif input[pointer] == 'a':
        pointer += 1
        return True
    else:
        return False


def proccess_B():
    global string_builder
    global pointer
    string_builder += 'B'
    if len(input) == 0 or pointer >= len(input):
        return True
    elif input[pointer] == 'c':
        pointer += 1
        if input[pointer] == 'c':
            pointer += 1
            if process_S():
                if input[pointer] == 'b':
                    pointer += 1
                    if input[pointer] == 'c':
                        pointer += 1
                        return True
        return False
    else:
        return True



def proccess_C():
    global string_builder
    global pointer
    string_builder += 'C'
    if proccess_A():
        if proccess_A():
            return True
    return False


def main(file):
    f = open(file, 'r')
    l = f.readlines()

    global string_builder
    string_builder = ''

    global pointer
    pointer = 0

    global input
    input = l[0].strip()

    result = process_S()

    if result and pointer == len(input):
        return string_builder + '\n' + 'DA' + '\n'
    else:
        return string_builder + '\n' + 'NE' + '\n'
