from flask import Flask
from flask import render_template

import json
import Pico
import HotTank, MashTank, BoilTank
import Regulation
import time

import Queue


app = Flask(__name__)
pico = Pico.Pico()

@app.route("/")
def main():
    return render_template('main.html')


@app.route("/temperature/<tank>.json")
def temperature(tank):
    history = []
    data = {}
    history.append( ["16:00","16:05","16:10","16:15","16:20","16:25"])
    if (tank == "hot"):
        data["value"]   = pico.hottank.last_value
        history.append(pico.hottank.temperatures.array)
    elif (tank == "mash"):
        data["value"]   = pico.mashtank.last_value
        history.append(pico.mashtank.temperatures.array)
    else:
        data["value"]   = pico.boiltank.last_value
        history.append(pico.boiltank.temperatures.array)

    data["history"] = history

    return json.dumps(data)


@app.route("/volume.json")
def volume():

    data = {}
    data["label"] = ["16:00","16:05","16:10","16:15","16:20","16:25"]
    data["hot"]   = [50,45,42,44,48,50]
    data["mash"]  = [20, 25, 30, 30, 30, 30, 30]
    data["boil"]  = [0, 0, 7, 12, 20, 20, 20]

    return json.dumps(data)

@app.route("/power.json")
def power():
    data = {}
    data["label"] = ["16:00","16:05","16:10","16:15","16:20","16:25"]
    data["hot"]   = [1100, 1200, 1300, 1640, 1480, 1400, 1520]
    data["mash"]  = [600,520,550,480,450,500]
    data["boil"]  = [600, 400, 1000, 600, 500, 900, 800]

    return json.dumps(data)


@app.route("/task.json")
def task():
    data = {}
    data["task"] = []
    data["task"].append ({
     "task name": "Fill in malt for Dark IPA",
     "status": "done"
     })

    data["task"].append ({
     "task name": "Fill in malt for bitter",
     "status": "waiting"
    })
    data["task"].append ({
     "task name": "Dump Dark IPA",
     "status": "unavailable"
    })
    data["task"].append ({
     "task name": "Fill in malt for Stout",
     "status": "unavalaible"
    })

    return json.dumps(data)

@app.route("/recipe.json")
def recipe():
    data = {}
    data["recipes"] = []
    data["recipes"].append({
    "recipe_name" : "Dark IPA",
    "step"        : "Boil",
    "time"        : "25m 10s",
    "status"      : "active"
    })

    data["recipes"].append({
    "recipe_name" : "Bitter",
    "step"        : "Mash",
    "time"        : "15m 56s",
    "status"      : "active"
    })

    data["recipes"].append({
    "recipe_name" : "Stout",
    "step"        : "",
    "time"        : "",
    "status"      : "pending"
    })

    return json.dumps(data)


@app.route("/valve.json")
def valve():
    data = {}
    data["switchs"] = []

    data["switchs"].append({
    "name"   :"valve-hot",
    "checked":True
    })
    data["switchs"].append({
    "name"   :"valve-mash",
    "checked":True
    })
    data["switchs"].append({
    "name"   :"valve-boil",
    "checked":True
    })

    return json.dumps(data)



@app.route("/resistor.json")
def resistor():
    data = {}
    data["switchs"] = []

    data["switchs"].append({
    "name"   :"resistor-hot",
    "checked":True
    })
    data["switchs"].append({
    "name"   :"resistor-mash",
    "checked":True
    })
    data["switchs"].append({
    "name"   :"resistor-boil",
    "checked":True
    })

    return json.dumps(data)


@app.route("/pump.json")
def pump():
    data = {}
    data["switchs"] = []

    data["switchs"].append({
    "name"   :"pump",
    "checked":True
    })

    return json.dumps(data)




app.debug = True
if __name__ == "__main__":

    hot =  HotTank.HotTank(saturation=50, period=1)

    start_boil_queue      = Queue.Queue()
    start_heat_queue      = Queue.Queue()

    start_counting_queue = Queue.Queue()
    need_cleaning_queue  = Queue.Queue()

    boil = BoilTank.BoilTank(start_heat_queue, start_boil_queue, start_counting_queue, need_cleaning_queue)

    start_mash_queue    = Queue.Queue()
    need_cleaning_queue = Queue.Queue()

    mash = MashTank.MashTank(hot, boil, start_mash_queue, need_cleaning_queue)

    regule = Regulation.Regulation(hot, mash, boil)
    pico.real_init(hot, mash, boil, regule)
    app.run()
