Sistema de Votação Simples 🗳️
Este repositório contém um sistema de votação básico apenas para prática/estudo desenvolvido com Flask para o backend (API) e HTML/CSS/JavaScript para o frontend (interface do usuário).

Backend (Python com Flask) 🐍
O backend é responsável por gerenciar as votações, registrar os votos e fornecer os resultados.

Dependências
Para rodar o backend, é necessário ter o Flask e o SQLite3 (que já vem incluso com o Python) instalados.

Para instalar o Flask, utilize o comando:

pip install Flask

Estrutura do Banco de Dados (SQLite) 💾
O sistema utiliza um arquivo database.db para persistir os dados. A inicialização do banco de dados cria três tabelas principais:

votacoes: Armazena os detalhes de cada votação.

id: Identificador único da votação.

titulo: Título da votação (ex: "Pesquisa de Opinião").

data_criacao: Carimbo de data/hora da criação da votação.

ativa: Status da votação (1 para ativa, 0 para inativa).

opcoes_voto: Contém as opções disponíveis para cada votação.

id: Identificador único da opção.

votacao_id: Chave estrangeira para a votação a qual a opção pertence.

nome_opcao: Texto da opção (ex: "Opção A").

votos: Registra cada voto individual.

id: Identificador único do voto.

votacao_id: Chave estrangeira para a votação.

opcao_id: Chave estrangeira para a opção votada.

ip_usuario: Endereço IP do usuário que votou (utilizado para evitar votos duplicados por IP na mesma enquete).

data_voto: Carimbo de data/hora do registro do voto.

Como Rodar o Backend ▶️
Salve o código Python do backend em um arquivo, por exemplo, app.py.

Abra o terminal na pasta onde o arquivo foi salvo.

Execute o arquivo:

python app.py

O servidor Flask será iniciado na porta 5000 (http://127.0.0.1:5000). O banco de dados e as tabelas serão criados automaticamente caso não existam.

Endpoints da API 🌐
O backend expõe os seguintes endpoints:

/ (GET)

Descrição: Serve a página HTML principal (index.html).

Exemplo de Uso: Acessar http://127.0.0.1:5000/ em um navegador.

/votacoes (POST)

Descrição: Cria uma nova votação.

Corpo da Requisição (JSON):

{
    "titulo": "Nome da Votação",
    "opcoes": ["Opção 1", "Opção 2", "Opção 3"]
}

Respostas: 201 Created (sucesso com o ID da votação) ou 400 Bad Request/500 Internal Server Error (erro).

/votacoes_ativas (GET)

Descrição: Retorna uma lista de todas as votações que estão ativas.

Resposta: Array de objetos JSON contendo id, titulo e data_criacao das votações.

/votar (POST)

Descrição: Registra um voto para uma opção em uma votação específica, impedindo votos duplicados pelo mesmo IP.

Corpo da Requisição (JSON):

{
    "votacao_id": 1,
    "opcao_id": 3
}

Respostas: 200 OK (voto registrado com sucesso), 400 Bad Request (IDs ausentes), 409 Conflict (usuário já votou) ou 500 Internal Server Error (erro).

/votacoes/<int:votacao_id>/resultados (GET)

Descrição: Exibe os resultados de uma votação específica, incluindo a contagem de votos para cada opção.

Exemplo de Uso: Para ver os resultados da votação com ID 1, acessar http://127.0.0.1:5000/votacoes/1/resultados.

Resposta: Objeto JSON com titulo_votacao e um array resultados contendo id, nome_opcao e total_votos para cada opção. Retorna 404 Not Found se a votação não for encontrada.

Frontend (HTML, CSS e JavaScript) 🎨
O frontend é a interface baseada em web que permite aos usuários criar novas votações.

Estrutura do Arquivo (index.html) 📄
HTML: Define a estrutura da página, que inclui um formulário para a criação de votações.

CSS: Aplica estilos visuais à página, utilizando um tema escuro e cores contrastantes para garantir boa legibilidade.

JavaScript: Implementa a lógica interativa, como:

Adição e remoção dinâmica de campos de entrada para opções de voto no formulário.

Validação de formulário para assegurar que há um mínimo de duas opções por votação.

Envio dos dados da nova votação para a API do backend.

Exibição de mensagens de feedback (sucesso ou erro) para o usuário na interface.

Como Usar a Interface 🧑‍💻
Título da Votação: Insira o título desejado para a votação no campo "Nome do grupo".

Opções de Voto: Preencha as opções disponíveis. É possível adicionar mais campos de opção usando o botão "Adicionar Opção" e remover campos existentes com o botão "Remover". É obrigatório que a votação tenha no mínimo duas opções.

Criar Votação: Clique no botão "Criar Votação" para enviar os dados e criar a nova votação no sistema.

Como Rodar o Sistema Completo 🚀
Para ter o sistema funcionando localmente:

Crie um diretório para o seu projeto.

Dentro deste diretório, salve o código Python do backend como app.py.

Crie uma subpasta chamada templates dentro do diretório do projeto.

Dentro da pasta templates, salve o código HTML do frontend como index.html.

Abra um terminal, navegue até o diretório raiz do seu projeto e execute o comando:

python app.py

Abra seu navegador web e acesse http://127.0.0.1:5000/.
