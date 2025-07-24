from flask import Flask, render_template, request, g
import sqlite3
import base64

DATABASE = 'restaurantes.db'
app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Optional: for dict-like row access
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        criacao_de_tabela = """
            CREATE TABLE IF NOT EXISTS restaurantes (
                id_restaurante INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                email TEXT,
                senha TEXT,
                imagem_principal BLOB
            )
        """

        tabela_filha = """
            CREATE TABLE IF NOT EXISTS comidas_restaurantes (
                id INTEGER PRIMARY KEY,
                restaurante_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                vegano INTEGER NOT NULL,
                vegetariano INTEGER NOT NULL,
                leite INTEGER NOT NULL,
                gluten INTEGER NOT NULL,
                foto BLOB,
                des TEXT NOT NULL,
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes (id_restaurante)
            )
        """

        cursor.execute(criacao_de_tabela)
        cursor.execute(tabela_filha)

        # Check if the default user exists before inserting
        cursor.execute("SELECT * FROM restaurantes WHERE email = ?", ("batata",))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO restaurantes (email, senha) VALUES (?, ?)", ("batata", "batata"))

        conn.commit()

init_db()

@app.route("/<restaurante>/")
def hello(restaurante):
    nome = restaurante
    return render_template("index.html", nome=nome)

@app.route("/cardapio", methods=["POST"])
def get_data(restaurante):
    # You'll want to add functionality here later
    return f"Cardápio for {restaurante}"

@app.route("/<restaurante>/adicionar_restricoes")
def print_data(restaurante):
    nome = restaurante
    return render_template("formulario.html", nome=nome)

@app.route("/pegar_comidas", methods=["POST"])
def pegar_comidas():
    lactose = 'lactose' in request.form
    gluten = request.form.get("gluten")
    vegetariano = request.form.get("vegetariano")
    restrictions = list()
    nome = request.form.get("nome")
    if request.form.get("vegano"):
        restrictions.append(1)
    else:
        restrictions.append(0)
    if lactose:
        restrictions.append(1)
    else:
        restrictions.append(0)
    if gluten:
        restrictions.append(1)
    else:
        restrictions.append(0)
    if vegetariano:
        restrictions.append(1)
    else:
        restrictions.append(0)

    print(restrictions)

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM comidas_restaurantes WHERE name = ?", (nome,))
    results = cursor.fetchall()

    comidas = list()
    for row in results:
        v = row[3]
        ve = row[4]
        le = row[5]
        gu = row[6]
        image = row[7]
        des = row[8]
        base64_img = base64.b64encode(image).decode('utf-8')
        comidas.append({
            "description": des,
            "vegano": v,
            "vegetariano": ve,
            "lactose": le,
            "gluten": gu,
            "foto": base64_img
        })

    return render_template("formulario.html", restricoes = restrictions, comidas=comidas)

if __name__ == "__main__":
    app.run(debug=True)
