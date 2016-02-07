import urllib,json
import pprint

class Recipe:

    def __init__(self, url):
        self.url = url
        self.mash_steps = []


    def fetch_recipe(self):
        # get recipe from brewtoad
        response = urllib.urlopen(self.url+".json")
        self.json = json.load(response)
        self.add_steps()
        #pprint.pprint (self.json)

    def add_steps(self):
        mashsteps = self.json["recipe_mash_steps"]
        self.batch_size = 1.2 * float(self.json["batch_size"]) # supose it is in liters
        #pprint.pprint (self.batch_size)
        for step in mashsteps:
            temperature = int(step["target_temperature"])
            if(not step["target_temperature_is_metric"]):
                temperature = int((temperature- 32)/1.8) # target is in celcuis
            step['duration']    = step["time"]
            step['temperature'] = temperature
            step['dump']        = False

            self.mash_steps.append(step)
            #print "Add mash step "+ str(step["time"])+" min at "+str(temperature)+" C"

        malt_amount = 0
        recipe_fermentables = self.json["recipe_fermentables"]
        for ferm in recipe_fermentables:
            malt_amount += ferm["amount"]

        self.malt_amount = malt_amount
        self.mash_steps[0]["water_volume"] = 2.75 * self.malt_amount

        self.mash_steps[-1]["dump"] = True

        # Add sparge
        spargenumber = 1
        for s in range(spargenumber):
            sparge = {"temperature" : 78,
                      "water_volume": (self.batch_size - self.mash_steps[0]["water_volume"])/spargenumber,
                      "duration": 10,
                      "dump":True}
            self.mash_steps.append(sparge)

        self.boil_time = self.json["boil_time"]
        #print "Boil time: " + str(self.boil_time)
        pass
