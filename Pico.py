import threading
import time
import Queue
import Recipe


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Pico:

    def __init__(self):
        pass


    def real_init( self, hottank, mashtank, boiltank, period=1):
        self.recipes = []
        self.PID     = []
        self.steps   = []
        self.history = []
        self.valves  = []
        self.period  = period

        self.hottank   = hottank
        self.boiltank  = boiltank
        self.mashtank  = mashtank

        self.start_boil_queue = boiltank.start_boil_queue
        self.start_mash_queue = mashtank.start_mash_queue

        self.mash_index = 0
        self.boil_index = 0
        self.run_thread = True


    def fetch_recipe(self, url_recipe):
        recipe = Recipe.Recipe(url_recipe)
        recipe.fetch_recipe()
        return recipe

    def add_recipe(self, recipe):
        self.hottank.push_volume(recipe.batch_size)

        self.recipes.append(recipe)


    def FillMashTankThread(self):
        while self.run_thread:
            if self.mash_index < len(self.recipes):
                for step in self.recipes[self.mash_index].mash_steps:
                    self.mashtank.push_steps(step)
                self.start_mash_queue.put(None) # go next recipe
                self.start_mash_queue.join() # blocking -- waiting to push next recipe
                self.mash_index += 1
            else:
                time.sleep(0.05) # waiting for a new recipe from user

    def FillBoilTankThread(self):
        while self.run_thread:
            if self.boil_index < len(self.recipes):
                #for step in self.recipes[self.boil_index].boil_steps:
                self.boiltank.push_steps({'temperature':98, 'duration':self.recipes[self.boil_index].boil_time}) # only one step considered -- no hop droper
                self.start_boil_queue.put(None) # go next recipe
                self.start_boil_queue.join() # blocking -- waiting to push next recipe
                self.boil_index += 1
            else:
                time.sleep(0.05) # waiting for a new recipe from user

    def start_threads(self):
        self.t1 = threading.Thread(target=self.FillMashTankThread, args=[])
        self.t2 = threading.Thread(target=self.FillBoilTankThread, args=[])
        self.t1.start()
        self.t2.start()
