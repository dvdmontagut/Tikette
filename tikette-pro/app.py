from flask import Flask, render_template, request
from random import randint
import requests
import json
import folium
import os

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
        if "artist" not in dic:
            return render_template('NameSearch.html')

        
 
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
        latitudes = {}
        longitudes = {}
        ciudades = {}

        if cuantos == 0:
            return render_template('NameSearch.html')
        for i in range(cuantos):
            # response['_embedded']['events'][i]
            nombres[i] = response['_embedded']['events'][i]['name']
            fotos[i] = response['_embedded']['events'][i]['images'][0]['url']
            ciudades[i] = response['_embedded']['events'][i]['_embedded']['venues'][0]['city']['name']
            fechas[i] = response['_embedded']['events'][i]['dates']['start']['localDate']
            if "localTime" in response['_embedded']['events'][i]['dates']['start']:
                horas[i] = response['_embedded']['events'][i]['dates']['start']['localTime']
            else:
                horas[i] = "---"
            latitudes[i] = response['_embedded']['events'][i]['_embedded']['venues'][0]['location']['latitude']
            longitudes[i] = response['_embedded']['events'][i]['_embedded']['venues'][0]['location']['longitude']
            links[i] = response['_embedded']['events'][i]['url']
       
        

        icons = {}
        iconTemp = ""
        weatherTexts = {}
        maxTemps = {}
        minTemps = {}
        
        for i in range(cuantos):
            r = requests.get("https://api.tutiempo.net/json/?lan=es&apid=asEqXzXXzaqtXSf&ll=" + latitudes[i]+","+longitudes[i])
            response = json.loads(r.text)
            if "day1" in response:
                iconTemp = response['day1']['icon']
                icons[i] = "https://v5i.tutiempo.net/wi/01/" + "80" + "/" + str(iconTemp) + ".png"
                weatherTexts[i] = response['day1']['text']
                maxTemps[i] = str(response['day1']['temperature_max']) + "ºC"
                minTemps[i] = str(response['day1']['temperature_min']) + "ºC"
            else:
                icons[i] = "No data"
                weatherTexts[i] = "No data"
                maxTemps[i] = "-ºC"
                minTemps[i] = "-ºC"
        
        map = folium.Map(
            location=[latitudes[0], longitudes[0]],
            zoom_start=5
        )

        for i in range(cuantos):
            popup = folium.Popup("<i>" + "Fecha: " + fechas[i] + "<br>" + "Hora: " + horas[i] + "</i>", max_width=100,min_width=100)
            folium.Marker(
                location=[latitudes[i], longitudes[i]],
                popup= popup,
                tooltip="" + nombres[i] + "  (" + str(i+1) + "/" + str(cuantos) +")" 
            ).add_to(map)

        mapID = randint(1, 50000)
        mapName = "map" + str(mapID) + '.html'
        map.save('templates/' + mapName)

        return render_template('NameSearch.html', cuantos=range(cuantos), nombres=nombres, fotos=fotos, fechas=fechas, ciudades = ciudades, 
                                horas=horas, links=links, latitudes=latitudes, longitudes=longitudes, mapName=mapName,
                                icons=icons, weatherTexts=weatherTexts, maxTemps=maxTemps, minTemps=minTemps, jsCiudades = json.dumps(ciudades),
                               jsNombres=json.dumps(nombres), jsFotos=json.dumps(fotos), jsFechas=json.dumps(fechas), jsHoras=json.dumps(horas),
                               jsLinks=json.dumps(links), jsLatitudes=json.dumps(latitudes), jsLongitudes=json.dumps(longitudes), total=cuantos, jsTotal=json.dumps(cuantos),
                               jsIcons=json.dumps(icons), jsWeatherTexts=json.dumps(weatherTexts), jsMaxTemps=json.dumps(maxTemps), jsMinTemps=json.dumps(minTemps))       
    else:
        return render_template('NameSearch.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
