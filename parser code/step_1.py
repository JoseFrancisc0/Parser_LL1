from .utils import line_formatting

def validate_and_extract_grammar(lines):
    rules = {}
    no_terminals = set()
    terminals = set()
    rules_productions = {} 

    count = 1

    for line in lines: 
        
        line = line_formatting(line)

        if not line:
            continue

        if '->' not in line:
            raise Exception(f"Error: Invalid Line (need '->'): '{line}'")

        lhs, rhs = map(str.strip, line.split('->',1))

        if lhs == '':
            raise Exception(f"Error: Rule without name in line {count}: '{line}'")
        if rhs == '':
            raise Exception(f"Error: Rule without production in line {count}: '{line}'")

        rules[count] = line
        no_terminals.add(lhs)
        count+=1

    for num, rule in rules.items():
       lhs, rhs = map(str.strip, rule.split('->', 1))
       
       options = rhs.split('|')

       if lhs not in rules_productions:
            rules_productions[lhs] =  {
           'Productions': [],
           'Produces_epsilon': False
        }

       for option in options:
            if any('|' in symbol and symbol != '|' for symbol in option.split()):
                raise Exception(f"Error: No space between symbols in the production rule {num}: '{option.strip()}'")
                
            symbols = option.strip().split()

            clean_symbols = [] # new

            if len(symbols) == 1 and symbols[0] == 'ε':
                rules_productions[lhs]['Produces_epsilon'] = True
                rules_productions[lhs]['Productions'].append('ε') # new
            else: # new
                for symbol in symbols:
                    
                    if symbol.startswith("'") and symbol.endswith("'"): # new
                        clean_symbol = symbol.strip("'")
                    else: # new
                        clean_symbol = symbol

                    clean_symbols.append(clean_symbol)
                    if clean_symbol != 'ε' and clean_symbol not in no_terminals:
                        terminals.add(clean_symbol)
                rules_productions[lhs]['Productions'].append(clean_symbols)

    return rules, sorted(no_terminals), sorted(terminals), rules_productions

def rule1_First(rules_productions, terminals):
    first = {nt: set() for nt in rules_productions}
    
    for t in terminals:
        first[t] = {t}

    print("\n=== Calculating Rule 1 of firsts (for terminals and no terminals) ===") # modified   
    
    for nt, data in rules_productions.items():
        for production in data['Productions']:

            first_symbol = production[0]
            if first_symbol in terminals:
                if first_symbol not in first[nt]:
                    first[nt].add(first_symbol)
                    print(f"    Rule 1: first({nt}) += '{first_symbol}' (initial terminal)") # modified
            else:
                print(f"    Rule 1: first({nt}) does not change because it starts with no terminal '{first_symbol}'") # modified

    print(f"\nFirst sets after Rule 1:") # modified
    for key in sorted(first):
        print(f"    first({key}) = {sorted(first[key])}") # modified
    return first

def rule2_and_rule3_First(rules_productions, terminals, first):
    changed = True
    iteration = 1
    
    print("\n=== Calculating Rule 2 and Rule 3 of firsts (for no terminals only) ===") # modified
    while changed:
        print(f"\n---- Iteration {iteration} ----")
        changed = False

        for nt, data in rules_productions.items():
            for production in data['Productions']:

                if isinstance(production, str): # new
                    print(f"    Production: {nt} -> {production}") # new
                else:
                    print(f"    Production: {nt} -> {' '.join(production)}")

                if production == 'ε': # new and modified...
                    if 'ε' not in first[nt]:
                        first[nt].add('ε')
                        changed = True
                        print(f"    Rule 3: Production derives ε directly. Added ε to first({nt})")
                        continue

                all_nullable = True
                for symbol in production:

                    if symbol == 'ε': # new...
                        continue

                    if symbol in terminals:
                        if symbol not in first[nt]:
                            first[nt].add(symbol)
                            changed = True
                            print(f"    Rule 2: Terminal '{symbol}' added to first({nt})") # modified
                        all_nullable = False
                        break

                    elif symbol in first:
                        to_add = first[symbol] - {'ε'}
                        new_adds = to_add - first[nt]
                        if new_adds:
                            first[nt].update(new_adds)
                            changed = True
                            print(f"    Rule 2: {new_adds} added to first({nt}) from first({symbol})") # modified
                        
                        if 'ε' not in first[symbol]:
                            all_nullable = False
                            break
                    
                    else:
                        print(f"    Warning: Symbol '{symbol}' not recognized as terminal or non-terminal") # new
                        all_nullable = False
                        break
                
                if all_nullable:
                    if 'ε' not in first[nt]:
                        first[nt].add('ε')
                        changed = True
                        print(f"    Rule 3: All symbols can derive ε. Added ε to first({nt})") # modified
        
        print(f"\nFirst sets after iteration {iteration}:") # modified
        for key in sorted(first):
            print(f"    first({key}) = {sorted(first[key])}") # modified
        iteration += 1

    return first

def rule1_Follow(rules_productions, no_terminals):
    follow = {nt: set() for nt in no_terminals}
    
    start_symbol = next(iter(rules_productions)) # new
    follow[start_symbol].add('$') # new

    print("\n=== Calculating Rule 1 of follows (for no terminals only) ===")
    print(f"    Start rule in grammar is: {start_symbol}")
    for nt in sorted(follow):
        print(f"    follow({nt}) = {follow[nt] if follow[nt] else '∅'}")
    return follow

def rule2_and_rule3_Follow(rules_productions, first, follow, no_terminals):
    changed = True
    iteration = 1

    print("\n=== Calculating Rule 2 and Rule 3 of follows (for no terminals only) ===")

    while changed:
        print(f"\n---- Iteration {iteration} ----")
        changed = False

        for lhs, data in rules_productions.items(): # note: lhs is B
            for production in data['Productions']:
                if isinstance(production, str):
                    print(f"    Production: {lhs} -> {production}")
                else:
                    print(f"    Production: {lhs} -> {' '.join(production)}")
                if production == 'ε':
                    continue

                for i, B in enumerate(production): # note: B is A like in the pdf of rules
                    if B not in no_terminals:
                        continue

                    beta = production[i+1:] if i+1 < len(production) else [] # note: ganma is beta (it tries to see the next tokens)

                    first_beta = set()
                    all_nullable = True

                    if not beta:
                        all_nullable = True
                    else:
                        for symbol in beta:
                            if symbol in first:
                                first_beta.update(first[symbol] - {'ε'})
                                if 'ε' not in first[symbol]:
                                    all_nullable = False
                                    break
                            else:
                                all_nullable = False
                                break
                    new_add = first_beta - follow[B]
                    if new_add:
                        follow[B].update(new_add)
                        changed = True
                        print(f"    Rule 2: Added {new_add} to follow({B}) from first({beta})")

                    if all_nullable:
                        new_add = follow[lhs] - follow[B]
                        if new_add:
                            follow[B].update(new_add)
                            changed = True
                            print(f"    Rule 3: Added {new_add} to follow({B}) from follow({lhs}) because beta is nullable or empty")
        
        print(f"\nFollow sets after iteration {iteration}:") 
        for nt in sorted(follow):
            symbols = ", ".join(sorted(follow[nt])) if follow[nt] else "∅"
            print(f"    follow({nt}) = {symbols}")

        iteration += 1

    return follow