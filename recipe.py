import urllib,json
import pprint

class Recipe:

    def __init__(self, url):
        self.url = url

        self.fetch_recipe()
        self.add_steps()

    def fetch_recipe(self):
        # get recipe from brewtoad
        response = urllib.urlopen(self.url+".json")
        self.json = json.load(response)
        #pprint.pprint (self.json)

    def add_steps(self):
        mash_steps = self.json["recipe_mash_steps"]
        #pprint.pprint (mash_steps)
        for step in mash_steps:
            temperature = int(step["target_temperature"])
            if(not step["target_temperature_is_metric"]):
                temperature = int((temperature- 32)/1.8) # target is in celcuis
            #print "Add mash step "+ str(step["time"])+" min at "+str(temperature)+" C"

        hop_steps = self.json["recipe_hops"]
        hop_time = 0
        for step in hop_steps:
            hop_time = max(hop_time, step["time"])
        #print "Boil time: " + str(hop_time)
        pass

recipe = Recipe("https://www.brewtoad.com/recipes/houblon-chouffe-aka-hopchewy")
