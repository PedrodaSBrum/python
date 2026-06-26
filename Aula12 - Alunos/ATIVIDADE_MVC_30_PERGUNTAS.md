# Atividade Aula 12 — Model, Controller e View (StreamFlix)

**Disciplina:** Python / Flask  
**Profª:** Janaína Duarte  
**Projeto:** `flask/Aula12/`  
**Objetivo:** Explorar o código, localizar arquivos e explicar o que cada camada faz.

---

## Como responder

1. Abra a pasta `flask/Aula12/` no editor ou GitHub.
2. Navegue pelas pastas `models/`, `controllers/` e `views/`.
3. Rode o site (`python app.py`) quando a pergunta pedir para testar no navegador.
4. Responda com **caminho do arquivo** + **explicação em suas palavras**.

**Identificação**

- Nome: Pedro da Silva Brum
- Turma: 3C2

---

## Bloco A — Model (perguntas 1 a 10)

**1.** Em qual pasta ficam as classes que representam tabelas do banco SQLite? Cite o caminho.

**R.**Aula12 - Alunos/models/ — é nessa pasta que estão os arquivos base.py, filme_favorito.py e historico_busca.py, cada um contendo uma classe que representa uma tabela do banco.

**2.** Qual é o nome do arquivo de banco criado quando o app roda? Em qual arquivo Python essa configuração está?

**R.** R. O arquivo de banco criado é streamflix.db. A configuração está em app.py, na linha: app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "streamflix.db")

**3.** Quais classes Model existem no projeto (nome das classes)? Em quais arquivos `.py` cada uma está?

**R.** Existem três classes Model (excluindo o __init__.py que é apenas importação):
ModeloBase → models/base.py
FilmeFavorito → models/filme_favorito.py
HistoricoBusca → models/historico_busca.py

**4.** De qual superclasse `FilmeFavorito` e `HistoricoBusca` herdam? O que elas ganham automaticamente por herança (cite 3 campos)?

**R.**Ambas herdam de ModeloBase (definida em models/base.py). Por herança, ganham automaticamente os campos:

id — chave primária inteira
data_criacao — data/hora de criação do registro
data_atualizacao — data/hora da última atualização do registro

**5.** Qual é o `__tablename__` da tabela de favoritos? Por que usamos `__tablename__` em vez de só o nome da classe?

**R.**O __tablename__ é "filmes_favoritos" (definido em models/filme_favorito.py). Usamos __tablename__ porque o SQLAlchemy precisa saber o nome exato da tabela no banco de dados. Sem ele, o ORM tentaria inferir o nome a partir da classe (que viraria algo como filme_favorito), o que pode causar inconsistências. Com __tablename__ definimos explicitamente o nome que queremos no SQLite.

**6.** No model `FilmeFavorito`, qual coluna guarda o id do filme vindo da API TMDB? Ela tem alguma restrição especial (`unique`, `nullable`)?

**R.**A coluna é tmdb_id. Ela tem duas restrições:

nullable=False — o campo é obrigatório, não pode ser nulo
unique=True — não pode haver dois favoritos com o mesmo ID da TMDB, evitando duplicatas

**7.** Abra `models/filme_favorito.py`. O que o método `@classmethod adicionar` faz passo a passo? O que acontece se o filme já existir nos favoritos?

**R.**O método adicionar funciona assim passo a passo:

Chama cls.buscar_por_tmdb(tmdb_id) para verificar se o filme já existe no banco;
Se o filme já existir, retorna None imediatamente — sem fazer nada;
Se o filme não existir, cria uma instância de FilmeFavorito com os dados recebidos (tmdb_id, titulo, poster_path, nota, ano);
Adiciona o objeto à sessão com db.session.add(fav);
Confirma a gravação com db.session.commit();
Retorna o objeto salvo;

**8.** Onde está o método que lista as últimas 8 buscas? Qual é o nome da classe e do método?

**R.** O método está em models/historico_busca.py, na classe HistoricoBusca, método ultimas. Ele recebe um parâmetro limite com valor padrão 8 e retorna as buscas mais recentes ordenadas pela data_criacao de forma decrescente.

**9.** O model grava dados da API TMDB inteira ou só alguns campos espelhados? Cite 4 campos salvos em `FilmeFavorito`.

**R.**O model grava apenas alguns campos espelhados da API (não tudo). Os 4 campos salvos são:

tmdb_id — ID do filme na API TMDB
titulo — título do filme
poster_path — caminho da imagem do pôster
nota — nota/avaliação do filme
(também há ano)

**10.** Em `models/__init__.py`, o que é exportado além de `db`? Por que o controller importa `from models import FilmeFavorito` em vez de importar o arquivo inteiro da pasta?

**R.**Além de db, são exportados ModeloBase, FilmeFavorito e HistoricoBusca (listados no __all__). O controller importa from models import FilmeFavorito em vez de from models.filme_favorito import FilmeFavorito porque o __init__.py da pasta models centraliza todas as exportações — funciona como uma "vitrine" do pacote. Assim o controller não precisa saber em qual arquivo interno cada classe está; tudo vem de um único ponto (models), o que facilita manutenção e refatoração.

---

## Bloco B — Controller (perguntas 11 a 20)

**11.** Quantos Blueprints existem no projeto? Cite o **nome** de cada um e o **url_prefix** (se tiver).

**R.**Existem 3 Blueprints:

dashboard_bp — nome "dashboard", sem url_prefix (responde na raiz /)
filmes_bp — nome "filmes", url_prefix="/filmes"
favoritos_bp — nome "favoritos", url_prefix="/favoritos"

**12.** Em qual arquivo está a rota `/filmes/populares`? Qual é o nome da função Python que responde essa URL?

**R.**A rota /filmes/populares está em controllers/filmes_controller.py. A função Python que responde essa URL é populares().

**13.** O que a função `populares()` faz antes de chamar `render_template`? Cite duas chamadas (Model, Service ou API).

**R.**Antes de chamar render_template, a função populares() faz:

api.filmes_populares() — chama o Service TmdbApi para buscar a lista de filmes populares na API TMDB
FilmeFavorito.listar() — chama o Model para obter todos os favoritos salvos no banco local (para saber quais já foram marcados como favorito)

**14.** Quando o usuário busca um filme em `/filmes/buscar`, qual controller registra o termo no banco? Qual model é usado e em qual linha aproximada?

**R.**O controller filmes_controller.py (Blueprint filmes_bp) registra a busca. Após obter os resultados da API, chama HistoricoBusca.registrar(termo, len(filmes)) — está dentro da função buscar(), na parte que verifica if termo:. O model usado é HistoricoBusca.

**15.** Abra `controllers/favoritos_controller.py`. Qual método HTTP é exigido para adicionar favorito (`GET` ou `POST`)? Qual a URL completa de exemplo para adicionar o filme id 550?

**R.**O método exigido é POST (methods=["POST"] na rota /adicionar/<int:tmdb_id>). A URL completa de exemplo para adicionar o filme de id 550 seria: POST /favoritos/adicionar/550

**16.** No `filmes_controller.py`, rota `detalhe(filme_id)`: o que acontece se `api.detalhe(filme_id)` retornar `None`?

**R.**Se api.detalhe(filme_id) retornar None, o controller executa return redirect(url_for("filmes.populares")) — ou seja, redireciona o usuário para a página de filmes populares em vez de tentar renderizar uma página de detalhe com dados inexistentes.

**17.** Onde os Blueprints são **registrados** no Flask? Cite o arquivo e o comando usado (3 registros).

**R.**Os Blueprints são registrados em app.py, dentro da função criar_app(), com os comandos:

app.register_blueprint(dashboard_bp)
app.register_blueprint(filmes_bp)
app.register_blueprint(favoritos_bp)

**18.** Qual controller cuida da página inicial `/`? Quais variáveis ele envia para o template `index.html`?

**R.**A página inicial / é cuidada pelo dashboard_controller.py (Blueprint dashboard_bp), função index(). As variáveis enviadas ao template são:

populares — primeiros 6 filmes populares
melhores — primeiros 6 melhores filmes
total_favoritos — quantidade de favoritos salvos no banco
historico — últimas 5 buscas feitas
modo_demo — booleano indicando se está em modo demonstração

**19.** A pasta `services/tmdb_api.py` é Model, Controller ou View? Justifique: quem chama essa classe e para quê?

**R.**É um Service (camada de serviço), não se encaixa exatamente em nenhum dos três do MVC clássico. Quem chama a classe TmdbApi são os Controllers (dashboard_controller.py, filmes_controller.py), para consultar dados externos da API TMDB (filmes populares, melhores, busca, detalhes, streaming). O Service isola a lógica de comunicação com a API externa, deixando o controller apenas orquestrando o fluxo.

**20.** No controller de busca, de onde vem o termo digitado quando o usuário usa o formulário da home (`index.html`)? É `request.form` ou `request.args`? Explique a diferença nesse projeto.

**R.**Quando vem da home, o termo é obtido via request.args.get("q") (método GET). O formulário da home envia os dados pela URL (query string), enquanto um formulário POST enviaria pelo corpo da requisição. No código da função buscar(), há suporte para os dois casos: se o método for POST, usa request.form.get("q"); caso contrário (GET), usa request.args.get("q"). A diferença é que request.args lê parâmetros da URL (?q=batman) e request.form lê dados enviados no corpo da requisição HTTP.

---

## Bloco C — View (perguntas 21 a 30)

**21.** Onde ficam os templates HTML? Qual caminho completo da pasta?

**R.**Os templates ficam em Aula12 - Alunos/views/templates/. Essa pasta é configurada no app.py com template_folder="views/templates".

**22.** Qual template é a “base” de todas as páginas (layout com menu)? Como os outros templates usam esse layout (qual comando Jinja)?

**R.** O template base é views/templates/layout.html. Os outros templates o utilizam com o comando Jinja {% extends "layout.html" %} no início do arquivo e preenchem o conteúdo dentro do bloco {% block content %}...{% endblock %}.

**23.** Abra `views/templates/layout.html`. Liste os 5 links do menu e o `url_for` de cada um.

**R.**Os links do menu são:

StreamFlix (marca/logo) → url_for('dashboard.index') → /
Populares → url_for('filmes.populares') → /filmes/populares
Melhores → url_for('filmes.melhores') → /filmes/melhores
Buscar → url_for('filmes.buscar') → /filmes/buscar
Favoritos → url_for('favoritos.listar') → /favoritos/

**24.** Qual arquivo HTML exibe a seção **“Onde assistir (Brasil)”**? De onde vem a variável `streaming` usada nessa tela?

**R.**A seção é exibida em views/templates/filmes/detalhe.html. A variável streaming vem do controller filmes_controller.py, função detalhe(filme_id), que chama api.streaming(filme_id) no Service TmdbApi e passa o resultado para o template via render_template(..., streaming=streaming, ...).

**25.** O arquivo `filmes/_card.html` é uma página inteira ou um pedaço reutilizado? Quem inclui esse arquivo e com qual tag Jinja?

**R.**É um pedaço reutilizado (partial/componente). Ele representa o card visual de um filme e é incluído por outros templates (como filmes/lista.html) com a tag Jinja {% include 'filmes/_card.html' %}, evitando repetição de código HTML para exibir cada filme.

**26.** Em `filmes/detalhe.html`, como a View sabe se o filme já está nos favoritos? Qual variável booleana/objeto controla o botão “Salvar” vs “Remover”?

**R.**A View usa a variável favorito, que é um objeto FilmeFavorito (ou None caso o filme não esteja nos favoritos). No template há um {% if favorito %}: se favorito tiver valor (objeto encontrado no banco), exibe o botão "Remover dos favoritos"; caso contrário, exibe o botão "Salvar favorito". Essa variável é enviada pelo controller filmes_controller.py via FilmeFavorito.buscar_por_tmdb(filme_id).

**27.** Onde está o CSS do site? Como o `layout.html` carrega esse arquivo (função Flask/Jinja)?

**R.**O CSS está em views/static/css/style.css. O layout.html carrega esse arquivo com a função url_for do Flask/Jinja:

<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

**28.** Na listagem de favoritos (`favoritos/lista.html`), qual loop Jinja percorre os registros? Cite 3 campos exibidos na tabela.

**R.**O loop Jinja é {% for fav in favoritos %}...{% endfor %}. Três campos exibidos na tabela:

fav.titulo — nome do filme (como link para o detalhe)
fav.nota — avaliação com ★
fav.data_criacao — data em que foi salvo, formatada com .strftime('%d/%m/%Y')
(também há fav.ano)

**29.** O que significa `{% if modo_demo %}` no layout? Quem disponibiliza essa variável para **todos** os templates?

**R.**O bloco {% if modo_demo %} exibe um aviso em faixa amarela informando que o app está rodando sem uma chave de API TMDB válida, usando dados de demonstração. A variável modo_demo é disponibilizada para todos os templates pelo context_processor definido em app.py:

@app.context_processor
def inject_globals():
    from services import TmdbApi
    return {"modo_demo": TmdbApi().usando_demo}

**30.** Desenhe ou descreva o fluxo completo quando o aluno clica em **“Salvar favorito”** no detalhe do filme, indicando **View → Controller → Model** (e redirect de volta). Cite arquivos envolvidos.

**R.**
detalhe.html (clique)
  → POST /favoritos/adicionar/550
    → favoritos_controller.py :: adicionar()
      → FilmeFavorito.adicionar() [models/filme_favorito.py]
        → db.session.commit() → streamflix.db
      → redirect(/filmes/550)
    → filmes_controller.py :: detalhe()
      → FilmeFavorito.buscar_por_tmdb(550) [retorna o objeto salvo]
  → detalhe.html (botão agora é "Remover")

---

## Entrega

- Arquivo `.txt` ou `.md` com as 30 respostas 

**Critério:** respostas que mostrem que você **abriu o código**, não chute.

Boa exploração!
