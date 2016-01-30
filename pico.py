import threading
import time
import Queue

class Singleton(object):
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(*args, **kwargs)
        return cls.instance

class Pico(Singleton):
    def __init__(self, period=1):
        self.recipes = []
        self.PID     = []
        self.steps   = []
        self.history = []
        self.valves  = []
        self.period  = period

        self.start_heat_queue = Queue.Queue()
        self.start_boil_queue = Queue.Queue()

        self.hottank   = HotTank.HotTank()
        self.boiltank  = BoilTank.BoilTank(self.start_heat_queue, self.start_boil_queue)
        self.mashtank  = MashTank.MashTank(self.hottank, self.boiltank)

        self.mash_index = 0
        self.boil_index = 0

    def fetch_recipe(self, url_recipe):
        recipe = Recipe(url_recipe)
        recipe.fetch_recipe()
        return recipe

    def add_recipe(self, recipe):
        self.hottank.push_volume(recipe.boil_size)

        self.recipes.append(recipe)


    def FillMashTankThread(self):
        while True:
            if self.mash_index < len(self.recipes):
                for step in self.recipes[self.mash_index].mash_steps
                    self.mashtank.push_steps(step)
                self.start_mash_queue.put(None) # go next recipe
                self.start_mash_queue.join() # blocking -- waiting to push next recipe
                self.mash_index += 1
            else
                time.sleep(0.05) # waiting for a new recipe from user

    def FillBoilTankThread():
        while True:
            if self.boil_index < len(self.recipes):
                for step in self.recipes[self.boil_index].boil_steps
                    self.boiltank.push_steps(step)
                self.start_boil_queue.put(None) # go next recipe
                self.start_boil_queue.join() # blocking -- waiting to push next recipe
                self.boil_index += 1
            else
                time.sleep(0.05) # waiting for a new recipe from user

    def start_threads(self):
        self.t1 = threading.Thread(target=FillMashTankThread, args=[])
        self.t2 = threading.Thread(target=FillBoilTankThread, args=[])
        t1.start()
        t2.start()
