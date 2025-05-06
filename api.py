from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from collections import OrderedDict
from lucho.main import LL1_VALIDATE_GRAMMAR, LL1_PARSE_STRING

app = Flask(__name__)
CORS(app)

@app.route('/api/validate_grammar', methods=['POST'])
def validate_grammar():
    data = request.get_json()
    if not data or 'grammar' not in data:
        return jsonify({'error': 'Missing grammar in the request'}), 400

    try:
        result = LL1_VALIDATE_GRAMMAR(data['grammar'])

        if isinstance(result['rules_productions'], dict):
            ordered_rules_prod = list(OrderedDict(result['rules_productions']).items())
        else:
            ordered_rules_prod = result['rules_productions']

        ordered_parse_table = []
        for nonterminal, row in result['parsing_table'].items():
            for terminal, production in row.items():
                ordered_parse_table.append((nonterminal, terminal, production))

        return jsonify({
            'rules': result['rules'],
            'no_terminals':  result['no_terminals'],
            'terminals': result['terminals'],
            'rules_productions': ordered_rules_prod,
            'parsing_table': ordered_parse_table,
            'first_table': result['first_table'],
            'follow_table': result['follow_table'],
            'parse_tablita': result['parse_tablita'],
            'error_tablita': result['error_tablita']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/parse_string', methods=['POST'])
def parse_string():
    data = request.get_json()
    if not data or 'input_str' not in data:
        return jsonify({'error': 'Missing input string in the request'}), 400

    try:
        result = LL1_PARSE_STRING(data['terminals'], data['parsing_table'], data['rules_productions'], data['input_str'])
        return jsonify({
            'parsing_str_table': result['parsing_tabb']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)