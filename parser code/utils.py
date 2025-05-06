import unicodedata
from prettytable import PrettyTable

def line_formatting(line):
    line = unicodedata.normalize('NFKC', line) 
    line = line.replace('\u200b', '') 
    line = line.replace('‘', "'").replace('’', "'") 
    return line.strip()

def print_grammar_components(rules, no_terminals, terminals, rules_productions):
    print("Rules:")
    for rule in sorted(rules):
        print(f"   {rule}: {rules[rule]}")
    print("\n No Terminals:")
    print(" ", ", ".join(no_terminals))
    print("\n Terminals:")
    print(" ", ", ".join(terminals))
    print("\n No terminals productions:")
    for nt, content in rules_productions.items():
        print(f"\n {nt}:")
        for prod in content['Productions']:
            print(f"   -> {' '.join(prod)}")
        if content['Produces_epsilon']:
            print(f"   -> ε")
    
def print_first_sets_table(first, rules_productions, terminals):
    table_nt = PrettyTable()
    table_nt.field_names = ["No Terminal", "First"]
    for nt in sorted(rules_productions.keys()):
        symbols = ", ".join(sorted(first[nt])) if first[nt] else "∅"
        table_nt.add_row([nt, symbols])

    #print("\n First of no terminals:")
    return table_nt

    r"""
    table_t = PrettyTable()
    table_t.field_names = ["Terminal", "First"]
    for t in sorted(terminals):
        symbols = ", ".join(sorted(first[t])) if t in first else "∅"
        table_t.add_row([t, symbols])

    print("\n First of terminals:")
    print(table_t)
    """
    
def print_follow_sets_table(follow):
    table = PrettyTable()
    table.field_names = ["No Terminal", "Follow"]

    for nt in sorted(follow):
        symbols = ", ".join(sorted(follow[nt])) if follow[nt] else "∅"
        table.add_row([nt, symbols])

    #print("\n Follow of no terminals:")
    return table

def print_parsing_table(parsing_table):
    #print("\n=== LL1 Parsing Table: ===")
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
            if entries:
                formatted = ' | '.join(
                    '-' if prod in ['extract', 'explore']
                    else f"{nt} -> {prod}" if isinstance(prod, str) 
                    else f"{nt} -> {' '.join(prod)}"
                    for prod in entries
                )
                row.append(formatted)
            else:
                row.append('-')
        x.add_row(row)
    
    return x

def print_error_table(parsing_table):
    #print("\n=== LL1 Error Recovery Table: ===")
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
            if entries:
                formatted = ' | '.join(
                    prod if prod in ['extract', 'explore']
                    else '-'
                    for prod in entries
                )
                row.append(formatted)
            else:
                row.append('-')
        x.add_row(row)
    
    return x

def print_parsing_string_table(steps):
    table = PrettyTable()
    table.field_names = ["Stack", "Input String", "Action"]

    for step in steps:
        table.add_row([step['Stack'], step['Input String'], step['Action']])
    
    return table