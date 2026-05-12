'''
Aula 2

Criação de currículo utilizando flask'''

from flask import Flask

app = Flask(__name__)

# Definimos o HTML e o CSS em uma variável (String Multi-linha)
PAGINA_CURRICULO = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Meu Currículo Flask</title>
    <style>
        body { font-family: sans-serif; line-height: 1.6; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f4f9; }
        .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
        h2 { color: #3498db; margin-top: 25px; }
        .contato { font-style: italic; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Pedro da Silva Brum</h1>
        <p class="contato">E-mail: pbrum.dev@gmail.com | LinkedIn: /in/seuusuario</p>
        
        <h2>Objetivo</h2>
        <p>Desenvolvedor focado em Python e Flask buscando novas oportunidades.</p>
        
        <h2>Habilidades</h2>
        <ul>
            <li>Python (Flask)</li>
            <li>Bancos de Dados SQL</li>
            <li>Desenvolvimento de APIs</li>
        </ul>

        <h2>Experiência</h2>
        <p><strong>Colégio Santa Maria Minas</strong> - estágiario em Informatica (2025 - 2026)<br>
        Responsável pela manutenção de sistemas.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return PAGINA_CURRICULO

if __name__ == '__main__':
    app.run(debug=True)