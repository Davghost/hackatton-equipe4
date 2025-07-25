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
                name TEXT NOT NULL,
                description TEXT,
                email TEXT,
                senha TEXT,
                imagem_principal BLOB
            )
        """

        tabela_filha = """
            CREATE TABLE IF NOT EXISTS comidas_restaurantes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                vegano INTEGER NOT NULL,
                vegetariano INTEGER NOT NULL,
                leite INTEGER NOT NULL,
                gluten INTEGER NOT NULL,
                foto BLOB,
                des TEXT NOT NULL
            )
        """

        cursor.execute(criacao_de_tabela)
        cursor.execute(tabela_filha)

        # Check if the default user exists before inserting
        cursor.execute("SELECT * FROM restaurantes WHERE name = ?", ("restaurante",))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO restaurantes (name, email, senha) VALUES (?, ?, ?)", ("restaurante", "restaurante", "restaurante"))

        name = "burger.jpeg"

        with open(name, "rb") as file:
            blobData = file.read()

        conn.execute(
            "INSERT INTO comidas_restaurantes (des, foto, name, vegano, vegetariano, leite, gluten) VALUES (?,?,?,?,?,?,?)", ("hamburger", blobData, "restaurante", 1, 1, 0, 1,)
        )

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
    print(nome)
    if request.form.get("vegano"):
        restrictions.append(1)
    else:
        restrictions.append(0)
    if vegetariano:
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

    print(restrictions)

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM comidas_restaurantes WHERE name = ?", (nome,))
    results = cursor.fetchall()

    comidas = list()
    for row in results:
        v = row[2]
        ve = row[3]
        le = row[4]
        gu = row[5]
        image = row[6]
        des = row[7]
        base64_img = base64.b64encode(image).decode('utf-8')

        print(des)

        continuar = True
        print(v)
        print(restrictions[0])
        if v == 1 and restrictions[0] == 1:
            continuar = False
        if ve == 1 and restrictions[1] == 1:
            continuar = False
        if le == 1 and restrictions[2] == 1:
            continuar = False
        if gu == 1 and restrictions[3] == 1:
            continuar = False

        if continuar:
            print("oi")
            comidas.append({
                "description": des,
                "vegano": v,
                "vegetariano": ve,
                "lactose": le,
                "gluten": gu,
                "image_data": base64_img
            })

    return render_template("cardapio.html", restricoes = restrictions, comidas=comidas)

if __name__ == "__main__":
    app.run(debug=True)
