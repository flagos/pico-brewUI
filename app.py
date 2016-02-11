from flask import Flask
from flask import render_template

import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')


@app.route("/temperature/<tank>.json")
def temperature(tank):
    history = []
    data = {}
    history.append( ["16:00","16:05","16:10","16:15","16:20","16:25"])
    if (tank == "hot"):
        data["value"]   = 78
        history.append([68,68,68,72,78,98])
    elif (tank == "mash"):
        data["value"]   = 83
        history.append([68,68,68,72,78,79])
    else:
        data["value"]   = 98
        history.append([68,68,68,72,78,80])

    data["history"] = history

    return json.dumps(data)


@app.route("/volume.json")
def volume():

    data = {}
    data["label"] =  ["16:00","16:05","16:10","16:15","16:20","16:25"]
    data["hot"] =  [50,45,42,44,48,50]
    data["mash"] = [20, 25, 30, 30, 30, 30, 30]
    data["boil"] = [0, 0, 7, 12, 20, 20, 20]

    return json.dumps(data)

app.debug = True
if __name__ == "__main__":
    app.run()
