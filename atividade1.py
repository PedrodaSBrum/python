#Crie uma aplicação Flask que contenha uma rota específica responsável por explicar o conceito de decorator em Python.
#Requisitos
#Crie uma rota acessível por meio do caminho: /decorator
#Ao acessar essa rota no navegador, deve ser exibido um texto explicando:
#O que é um decorator em Python
#Para que ele serve
#Como ele é utilizado no Flask (exemplo: @app.route)

from flask import Flask

app = Flask(__name__)

@app.route('/decorator')
def explicando_decorator():
    return '''
        <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Decorator</title>
            </head>
            <body>
                <h1>O que é um decorator em Python</h1>

                <h2>É uma função que permite adicionar novas funcionalidades a outra função ou método sem precisar modificar o seu código original.</h2>
                
                <h1>Para o que serve o decorator </h1>
                <h2>Separar a lógica principal do código de tarefas auxiliares ou repetitivas.</h2>

                <h1>Como ele é utilizado no Flask (exemplo: @app.route)</h1>
                <h2>Serve para mapear uma URL do navegador a uma função específica no seu código Python</h2>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)