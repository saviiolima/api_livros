from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def inicializar_banco():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                imagem_url TEXT NOT NULL
            )
        """)
    print("Banco de dados criado com sucesso!")


inicializar_banco()


@app.route('/')
def pagina_inicial():
    return '<h2>Bem-vindo à Biblioteca Virtual! Doe e descubra novos livros.</h2>'


@app.route("/doar", methods=['POST'])
def doar_livro():
    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    imagem_url = dados.get("imagem_url")

    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({'erro': 'Todos os campos são obrigatórios!'}), 400

    with sqlite3.connect('database.db') as conn:
        conn.execute("""
            INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
            VALUES (?, ?, ?, ?)
        """, (titulo, categoria, autor, imagem_url))
        conn.commit()

    return jsonify({'mensagem': 'Livro cadastrado com sucesso!'}), 201


@app.route("/livros", methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

    lista_livros = [
        {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagem_url": livro[4]
        }
        for livro in livros
    ]

    return jsonify(lista_livros), 200


if __name__ == '__main__':
    app.run(debug=True)
