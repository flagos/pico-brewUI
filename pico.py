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


    def add_recipe(self, url_recipe):
        recipe = Recipe(url_recipe)

        self.hottank.push_volume(recipe.boil_size)

        self.recipes.append(recipe)


    def automate(self):
        recipe_mash = None
        recipe_boil = None
        while True:
            if not recipes:
                if self.mashtank.is_tank_in_use() is False:

                pass
            time.sleep(self.period)
