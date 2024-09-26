import http.client
from flask import Flask, json, jsonify, render_template


app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/assets')

# Ruta principal para el Home
@app.route('/')
def index():
    # Hacer la petición para obtener partidos en vivo
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": "11ad5f439755ea3775a46bd3736c4255"  # Asegúrate de usar tu propia clave API
    }

    conn.request("GET", "/fixtures?live=all", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # Convertir la respuesta en JSON
    parsed_data = json.loads(data)
    live_matches = parsed_data.get('response', [])  # Obtenemos los partidos en vivo de la respuesta

    # Renderizamos el HTML y pasamos los datos de los partidos en vivo
    return render_template('index.html', live_matches=live_matches)

# Ruta del Blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Ruta de About Me
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)

