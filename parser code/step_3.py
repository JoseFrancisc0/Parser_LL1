from .utils import print_parsing_string_table

def parse_string(parsing_table, rules_productions, input_string):
    
    start_symbol = next(iter(rules_productions))

    stack = ['$']
    stack.insert(0, start_symbol)
    print(start_symbol)

    input_function = input_string.strip().split() + ['$']

    steps = []

    iteration = 1

    #print(f"\n=== Processing the input string ===")

    #print(f"Input string: {input_string}")

    while True:
        stack_str = ' '.join(stack[::-1])
        input_str = ' '.join(input_function)

        X = stack[0]
        a = input_function[0]

        if X == a:
            action = f"Match {a}"
            steps.append({'Stack': stack_str, 'Input String': input_str, 'Action': action})
            #print(f">>> Action: {action}")
            stack.pop(0)
            input_function.pop(0)
            if X == '$':
                iteration += 1
                action = "Accept"
                steps.append({'Stack': '', 'Input String': '', 'Action': action})
                #print(f"\n=== How the table looks like in row {iteration} ===")
                #print_parsing_string_table(steps)
                #print(f">>> Action: {action}")
                break
            continue

        elif X in parsing_table: 
            productions = parsing_table[X].get(a, [])
            if not productions: # this should not happen, probably, but it could help me for implement extract and explore later :D
                action = f"Error: No rule for M[{X}, {a}]"
                steps.append({'Stack': stack_str, 'Input String': input_str, 'Action': action})
                #print(f">>> Action: {action}")
                break
            else:
                production = productions[0]

                if production == "extract":
                    action = f"Extract: pop {X} from stack"
                    stack.pop(0)
                
                elif production == "explore":
                    action = f"Explore: skip input {a}"
                    input_function.pop(0)

                else:
                    stack.pop(0)
                    if production != 'ε':
                        symbols = production if isinstance(production, list) else [production]
                        for sym in reversed(symbols):
                            stack.insert(0, sym)
                        action = f"Apply {X} -> {' '.join(symbols)}"
                    else:
                        action = f"Apply {X} -> ε"

                steps.append({'Stack': stack_str, 'Input String': input_str, 'Action': action})
                #print(f">>> Action: {action}")
        
        else: # this should not happen but it could help me for implement extract and explore later :D
            action = f"Error: Unexpected symbol '{X}' in the stack"
            steps.append({'Stack': stack_str, 'Input String': input_str, 'Action': action})
            #print(f">>> Action: {action}")
            break

        #print(f"\n=== How the table looks like in iteration {iteration} ===")
        #print_parsing_string_table(steps)
        iteration += 1
    
    tablo = print_parsing_string_table(steps)
    return tablo