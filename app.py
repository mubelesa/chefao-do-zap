from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# SQLite
DATABASE = 'database.db' 

# Função para conectar o DB
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# função para inicializar o DB (cria tabelas se elas não existirem)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            ativa INTEGER DEFAULT 1
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opcoes_voto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            votacao_id INTEGER NOT NULL,
            nome_opcao TEXT NOT NULL,
            FOREIGN KEY (votacao_id) REFERENCES votacoes(id) ON DELETE CASCADE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            votacao_id INTEGER NOT NULL,
            opcao_id INTEGER NOT NULL,
            ip_usuario TEXT NOT NULL,
            data_voto DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (votacao_id) REFERENCES votacoes(id) ON DELETE CASCADE,
            FOREIGN KEY (opcao_id) REFERENCES opcoes_voto(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

# rota para o arquivo index.html
@app.route('/')
def serve_index():
    # etapa para diagnóstico: verifica o caminho do app e da pasta de templates
    print(f"Flask app root path: {app.root_path}")
    print(f"Flask template folder: {app.template_folder}")
    return render_template('index.html')

# rota para criar uma nova votação
@app.route('/votacoes', methods=['POST'])
def criar_votacao():
    data = request.get_json()
    titulo = data.get('titulo')
    opcoes = data.get('opcoes')

    if not titulo or not opcoes:
        return jsonify({"message": "Título e opções são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO votacoes (titulo) VALUES (?)", (titulo,))
        votacao_id = cursor.lastrowid

        for opcao_nome in opcoes:
            cursor.execute(
                "INSERT INTO opcoes_voto (votacao_id, nome_opcao) VALUES (?, ?)",
                (votacao_id, opcao_nome)
            )
        conn.commit()
        return jsonify({"message": "Votação criada com sucesso!", "votacao_id": votacao_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Erro ao criar votação: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# rota para listar todas as votações ativas
@app.route('/votacoes_ativas', methods=['GET'])
def listar_votacoes():
    conn = get_db_connection()
    cursor = conn.cursor() 

    try:
        cursor.execute("SELECT id, titulo, data_criacao FROM votacoes WHERE ativa = 1 ORDER BY data_criacao DESC")
        votacoes = cursor.fetchall()
        votacoes_dict = [dict(votacao) for votacao in votacoes] 
        return jsonify(votacoes_dict), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao listar votações: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# rota para votar em uma opção
@app.route('/votar', methods=['POST'])
def votar():
    data = request.get_json()
    votacao_id = data.get('votacao_id')
    opcao_id = data.get('opcao_id')
    ip_usuario = request.remote_addr

    if not votacao_id or not opcao_id:
        return jsonify({"message": "IDs de votação e opção são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM votos WHERE votacao_id = ? AND ip_usuario = ?",
            (votacao_id, ip_usuario)
        )
        if cursor.fetchone()[0] > 0:
            return jsonify({"message": "Você já votou nesta enquete."}), 409

        cursor.execute(
            "INSERT INTO votos (votacao_id, opcao_id, ip_usuario) VALUES (?, ?, ?)",
            (votacao_id, opcao_id, ip_usuario)
        )
        conn.commit()
        return jsonify({"message": "Voto registrado com sucesso!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Erro ao registrar voto: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# rota para ver resultados de uma votação
@app.route('/votacoes/<int:votacao_id>/resultados', methods=['GET'])
def ver_resultados(votacao_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT titulo FROM votacoes WHERE id = ?", (votacao_id,))
        votacao_titulo = cursor.fetchone()
        if not votacao_titulo:
            return jsonify({"message": "Votação não encontrada."}), 404

        cursor.execute(
            """
            SELECT ov.id, ov.nome_opcao, COUNT(v.id) AS total_votos
            FROM opcoes_voto ov
            LEFT JOIN votos v ON ov.id = v.opcao_id AND v.votacao_id = ?
            WHERE ov.votacao_id = ?
            GROUP BY ov.id, ov.nome_opcao
            ORDER BY total_votos DESC, ov.nome_opcao ASC
            """,
            (votacao_id, votacao_id)
        )
        resultados = cursor.fetchall()
        resultados_dict = [dict(resultado) for resultado in resultados]

        return jsonify({
            "titulo_votacao": votacao_titulo['titulo'],
            "resultados": resultados_dict
        }), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar resultados: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# rodar servidor Flask
if __name__ == '__main__':
    init_db() 
    app.run(debug=True, port=5000)