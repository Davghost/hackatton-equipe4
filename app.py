from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/formulario")
def form():
    return render_template("formulario.html")

@app.route("/cardapio", methods=["POST"])
def cardapio():
    restricoes = request.form.getlist("restricoes")

    pratos = [
        {
            "nome": "Feijoada",
            "imagem": "feijoada.jpg",
            "restricoes": ["Vegano", "Vegetariano"]
        },
        {
            "nome": "Salada Vegana",
            "imagem": "salada_vegana.jpg",
            "restricoes": []
        },
        {
            "nome": "Lasanha Sem Gluten",
            "imagem": "lasanha.jpg",
            "restricoes": ["Leite", "Gluten", "Vegano", "Vegetariano"]
        },
        {
            "nome": "Hambúrguer Vegano",
            "imagem": "hamburguer_vegano.jpg",
            "restricoes": ["Gluten"]
        },
        {
            "nome": "Pizza Vegetariana",
            "imagem": "pizza.png",
            "restricoes": ["Gluten", "Vegano", "Leite"]
        },
        {
            "nome": "Frango",
            "imagem": "frango.png",
            "restricoes": ["Vegano","Vegetariano"]
        }
    ]

    pratos_filtrados = [
        prato for prato in pratos
        if not any(r in prato["restricoes"] for r in restricoes)
    ]
    return render_template("cardapio.html", pratos=pratos_filtrados, restricoes=restricoes)

@app.route("/salada")
def salada():
    return render_template("salada.html")

if __name__ == "__main__":
    app.run(debug=True)