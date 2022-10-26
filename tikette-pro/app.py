from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('NameSearch.html')

    dic = request.form
    tam = len(dic)
    if tam == 1:
        if "artist" in dic:
            argumentos = {'classificationName': 'music', 'keyword': dic['artist'],
                          'apikey': 'HNYtWPE0DGcjUFwmi0FBPTpbrZ3p7znK'}
            url = f"https://app.ticketmaster.com/discovery/v2/events.json"
            r = requests.get(url, params=argumentos)
            response = json.loads(r.text)

            cuantos = 20 if response['page']['totalElements'] > 20 else response['page']['totalElements']
            nombres = {}
            fotos = {}
            fechas = {}
            horas = {}
            links = {}
            for i in range(cuantos):
                # response['_embedded']['events'][i]
                nombres[i] = response['_embedded']['events'][i]['name']
                fotos[i] = response['_embedded']['events'][i]['images'][0]['url']
                fechas[i] = response['_embedded']['events'][i]['dates']['start']['localDate']
                horas[i] = response['_embedded']['events'][i]['dates']['start']['localTime']
                links[i] = response['_embedded']['events'][i]['url']
            return render_template('NameSearch.html', cuantos=range(cuantos), nombres=nombres, fotos=fotos, fechas=fechas,
                                   horas=horas, links=links)
        else:
            return render_template('NameSearch.html')


if __name__ == "__main__":
    app.run(debug=True)
