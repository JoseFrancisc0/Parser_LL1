# LL(1) PARSER

Integrantes:
- Luis Izaguirre
- Carlos Sobenes
- Jose Wong

## How to install
No hay plata para AWS, toco hacerlo local

1. Montas virtual environment de python
2. Instalas los siguientes paquetes
    - prettytable
    - psycopg2
    - flask
    - flask-cors
    - unicodedata (no me acuerdo si viene preinstalado o como)
3. Ejecutas api.py
4. Abres tu server local con el index.html

## Validando gramaticas

- Las reglas tienen que ser del siguiente formato: MAYUSCULA['] . Una sola letra mayuscula, opcionalmente una apostrofe a la derecha
- La gramatica debe de ser LL(1) compliant (nada de recursion o factorizacion a la izquierda)
- Puede seguir los modelos dentro de los archivos input_[]_grammar_LL1.txt

## Parseando strings

- Cada uno de los "tokens" del input deben de estar separados con espacios
- El scan_input() solo tokeniza las palabras desconocidas como id y numeros como num. No se sale de ahi
- Puede seguir los modelos dentro de los archivos input_[]_string_text.txt

Ejemplo:

"x=2+10;print(x)"          <--- BAD INPUT
"x = 2 + 10 ; print ( x )" <--- GOOD INPUT
"id = num + num ; print ( x )" <--- Tokenizado por el scaner

# IMPORTANTE : activar el autoplay del navegador para sonido

Si quiere, puede entrar al index.html, y reemplazar el color de fondo por algunas de las imagenes de la carpeta