from flask import Flask, render_template,request

app = Flask(__name__)

@app.get("/")
def index():
    return render_template('index.html')

@app.get("/formulario")
def form():
    return render_template("formulario.html")

@app.route("/cardapio", methods=["Post"]) 
 def cardapio() 
  restricoes= request.form.getlist
  ("restricoes")

  pratos = [
     {
      "nome": "feijoada" 
      "imagem" : "feijoada.jpg"
      "restricoes" : []
      },
      {
         "nome" : "salada Vegetariana"
         "imagem" : "salada.jpg"
         "restricoes" : ["Vegano", "Vegetariano", "Leite", "Gluten"]
      },
      {
         "nome" : "lasanha"
         "imagem" : "lasanha.jpg"
         "restricoes": ["Vegetariano", "Leite", "Gluten"]
      },
      {
         "nome" : "Hamburguer Vegano"
         "imagem" : "Hamburguer.jpg"
         "restricoes" : 
      }
       
        ]

if __name__ == '__main__':
    app.run(debug=True)