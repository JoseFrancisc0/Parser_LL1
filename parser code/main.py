from .step_1 import *
from .step_2 import *
from .step_3 import *
from .utils import *
import re

def scan_input(raw_input, terminals):
    tokens = []
    words = raw_input.strip().split()

    for word in words:
        if word.isnumeric():
            tokens.append('num')
        elif word in terminals:
            tokens.append(word)
        elif re.match(r"^[a-zA-Z_]\w*$", word):  # Identifier-like
            if word in terminals:
                tokens.append(word)
            else:
                tokens.append('id')
        else:
            # Check for individual symbol tokens (like ;, (, etc.)
            for char in word:
                if char in terminals:
                    tokens.append(char)
                else:
                    # Could throw an error here or assume it's part of a malformed id
                    tokens.append('id')
    
    processed = ""
    for word in tokens:
        processed = processed + word + " "

    return processed

def LL1_VALIDATE_GRAMMAR(grammar):
    rules, no_terminals, terminals, rules_productions = validate_and_extract_grammar(grammar)
    #print_grammar_components(rules, no_terminals, terminals, rules_productions)

    first = rule1_First(rules_productions, terminals)
    first = rule2_and_rule3_First(rules_productions, terminals, first)
    first_table = print_first_sets_table(first, rules_productions, terminals)
    #print(first_table)

    follow = rule1_Follow(rules_productions, no_terminals)
    follow = rule2_and_rule3_Follow(rules_productions, first, follow, no_terminals)
    follow_table = print_follow_sets_table(follow)
    #print(follow_table)

    parsing_table = create_parsing_table(rules_productions, first, follow, terminals)
    parse_tablita = print_parsing_table(parsing_table)
    
    error_tablita = print_error_table(parsing_table)

    return {
        'rules': rules,
        'no_terminals': no_terminals,
        'terminals': terminals,
        'rules_productions': rules_productions,
        'parsing_table': parsing_table,
        'first_table': str(first_table),
        'follow_table': str(follow_table),
        'parse_tablita': str(parse_tablita),
        'error_tablita': str(error_tablita)
    }

def LL1_PARSE_STRING(terminals, parsing_table, rules_productions, input_str):
    tokenized = scan_input(input_str, terminals)
    parsing_tabb = parse_string(parsing_table, rules_productions, tokenized)
    #print(parsing_tabb)

    return {
        'parsing_tabb': str(parsing_tabb)
    }

def LL1_PARSER(grammar, input_str):
    try:
        rules, no_terminals, terminals, rules_productions = validate_and_extract_grammar(grammar)
        #print_grammar_components(rules, no_terminals, terminals, rules_productions)

        first = rule1_First(rules_productions, terminals)
        first = rule2_and_rule3_First(rules_productions, terminals, first)
        first_table = print_first_sets_table(first, rules_productions, terminals)

        follow = rule1_Follow(rules_productions, no_terminals)
        follow = rule2_and_rule3_Follow(rules_productions, first, follow, no_terminals)
        follow_table = print_follow_sets_table(follow)

        parsing_table = create_parsing_table(rules_productions, first, follow, terminals)
        parse_tablita = print_parsing_table(parsing_table)
        
        error_tablita = print_error_table(parsing_table)

        tokenized = scan_input(input_str, terminals)
        parsing_tabb = parse_string(parsing_table, rules_productions, tokenized)

        return {
            'first_table': first_table,
            'follow_table': follow_table,
            'parse_tablita': parse_tablita,
            'error_tablita': error_tablita,
            'parsing_tabb': parsing_tabb
        }

    except Exception as e:
        print(e)

r"""
if __name__ == "__main__":
    grammar_dir = 'input_1_grammar_LL1.txt'
    input_str_dir = 'input_1_string_text.txt'

    with open(input_str_dir, 'r') as f:
        input_string = f.read().strip()

    with open(grammar_dir, 'r', encoding='utf-8') as f: 
        grammar = f.readlines()

    res = LL1_VALIDATE_GRAMMAR(grammar)

    aaaa = LL1_PARSE_STRING(res['terminals'], res['parsing_table'], res['rules_productions'], input_string)
"""