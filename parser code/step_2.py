from prettytable import PrettyTable

def create_parsing_table(rules_productions, first, follow, terminals):
    table = {}
    for nt in rules_productions:
        table[nt] = {t: [] for t in terminals}
        table[nt]['$'] = []

    print(f"\n=== Creating LL1 Parsing Table ===")

    for A, data in rules_productions.items():
        for production in data['Productions']:

            first_alpha = set()

            if isinstance(production, str) and production == 'ε':
                first_alpha.add('ε')
            else:
                for symbol in production:
                    first_alpha.update(first.get(symbol, set() - {'ε'}))
                    if 'ε' not in first.get(symbol, set()):
                        break
                else:
                    first_alpha.add('ε')

            for terminal in first_alpha - {'ε'}:
                if terminal in table[A]:
                    table[A][terminal].append(production)
                    print(f"    Rule 1: Added {production} to M[{A}, {terminal}]")

            if 'ε' in first_alpha:
                for terminal in follow[A]:
                    if terminal in table[A]:
                        table[A][terminal].append(production)
                        print(f"    Rule 2: Added {production} to M[{A}, {terminal}]")
    
    for A in table:
        for terminal in table[A]:
            if not table[A][terminal]:
                if 'ε' not in first[A] and terminal in follow[A]:
                    table[A][terminal] = ['extract']
                    print(f"    Error Recovery: Added 'extract' to M[{A}, {terminal}]")
                else:
                    table[A][terminal] = ['explore']
                    print(f"    Error Recovery: Added 'extract' to M[{A}, {terminal}]")
    return table

def create_error_table(first, follow, parsing_table):
    all_terminals = set()
    for row in parsing_table.values():
        all_terminals.update(row.keys())
    headers = [''] + sorted(all_terminals)

    x = PrettyTable()
    x.field_names = headers

    for nt, columns in parsing_table.items():
        row = [nt]
        for terminal in sorted(all_terminals):
            entries = columns.get(terminal, [])
            if entries or terminal in follow[nt]:
                row.append("E")
            else:
                row.append("X")
            
        x.add_row(row)
    
    print(x)
    return x

# FULL EXPLORE
# EXTRACT si hay en parsing table
# EXTRACT en FOLLOW()s