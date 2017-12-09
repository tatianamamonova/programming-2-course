import json
import os

import matplotlib.pyplot as plt
import numpy as np
import mpld3

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

def participants():
    f = open('data.json','r',encoding='utf-8')
    data = json.load(f)
    f.close()

    fig, axes = plt.subplots()
    toponims = set(data["from"])
    cities_dict = {toponim: 0 for toponim in toponims}

    for city in data["from"]:
        cities_dict[city] += 1

    cities = sorted(list(cities.dict.keys))
    participants = []

    for city in cities:
        participants.append(cities_dict[city])

    objects = cities
    y_pos = np.arange(len(cities))
	 
    plt.bar(y_pos, participants, align='center', alpha=0.5)
    plt.xticks(y_pos, cities)
    plt.ylabel('Кол-во респондентов')
    plt.title('Распределение респондентов по городам')

    return fig_to_html(fig)

@app.route('/')
def index():  
    if not os.path.isfile('data.json'):
        data = {"sex": [], "age": [], "born": [], "from": [], "job": []}
        for i in range(12):
            data[str(i+1)] = []
        f = open('data.json','w',encoding='utf-8')
        json.dump(data, f, ensure_ascii = False, indent = 4)
        f.close()
    
    if request.args:
        return survey()
    return render_template("index.html")

@app.route('/survey')
def survey():
    f = open('data.json','r',encoding='utf-8')
    data = json.load(f)
    f.close()
    
    for item in list(request.args.keys()):
        data[item].append(request.args[item])
    
    f = open('data.json','w',encoding='utf-8')
    json.dump(data, f, ensure_ascii = False, indent = 4)
    f.close()
    
#       return render_template("thankyou.html")
#       return "WHY DID I ENTER THIS IF"
    return render_template("survey.html")

@app.route('/thankyou')
def thankyou():
    f = open('data.json','r',encoding='utf-8')
    data = json.load(f)
    f.close()
    
    for item in list(request.args.keys()):
        data[item].append(request.args[item])
    
    f = open('data.json','w',encoding='utf-8')
    json.dump(data, f, ensure_ascii = False, indent = 4)
    f.close()
    return render_template("thankyou.html")

@app.route('/json')
def printjson():
    f = open('data.json','r',encoding='utf-8')
    return render_template("json.html", json_data = f.read())

@app.route('/stats')
def stats():
    return render_template("stats.html", bar_plot = participants())
	
if __name__ == '__main__':
    app.run(debug=True)
