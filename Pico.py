from future import standard_library
standard_library.install_aliases()
from builtins import object
import threading
import time
import queue

import Recipe


class Pico(object):

    def __init__(self):
        pass


    def real_init( self, hottank, mashtank, boiltank, regulation, period=1):
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

        self.regule = regulation

        self.data = {}
        self.data["task"] = []
        self.data["task"].append({
            "task name": "Fill in malt for Dark IPA",
            "status": "done"
        })
        
        self.data["task"].append({
            "task name": "Fill in malt for bitter",
            "status": "waiting"
        })
        self.data["task"].append({
            "task name": "Dump Dark IPA",
            "status": "unavailable"
        })
        self.data["task"].append({
            "task name": "Fill in malt for Stout",
            "status": "unavailable"
        })
        

    def add_task(self, recipe_name, task_name, status):
        '''Create a task, id in return'''
        self.data["task"].append({
            "recipe_name": recipe_name,
            "task_name": task_name,
            "status": status
        })
        return len(self.data["task"]) - 1

    def update_task(self, task_id, status):
        self.data["task"][task_id]["task_name"] = status

    def fetch_recipe(self, url_recipe):
        recipe = Recipe.Recipe(url_recipe)
        recipe.fetch_recipe()
        return recipe

    def add_recipe(self, recipe):
        self.hottank.push_volume(recipe.batch_size)
        recipe.id_ = self.add_task(recipe.name, "Fill malt for "+ str(recipe.name), "unavailable")
        self.recipes.append(recipe)


    def FillMashTankThread(self):
        while self.run_thread:
            if self.mash_index < len(self.recipes):
                self.mashtank.need_cleaning_queue.get()
                self.mashtank.need_cleaning_queue.task_done()  # keep it for testing
                self.current_recipe = self.recipes[self.mash_index]
                self.update_task(self.current_recipe.id_, "waiting")

                for step in self.current_recipe.mash_steps:
                    self.mashtank.push_steps(step)
                self.start_mash_queue.put(None)  # go next recipe
                self.start_mash_queue.join()  # blocking -- waiting to push next recipe
                self.mash_index += 1
            else:
                time.sleep(0.05)  # waiting for a new recipe from user

    def FillBoilTankThread(self):
        while self.run_thread:
            if self.boil_index < len(self.recipes):
                #for step in self.recipes[self.boil_index].boil_steps:
                self.boiltank.push_steps({'temperature':98, 'duration':self.recipes[self.boil_index].boil_time})  # only one step considered -- no hop droper
                self.start_boil_queue.put(None)  # go next recipe
                self.start_boil_queue.join()  # blocking -- waiting to push next recipe
                self.boil_index += 1
            else:
                time.sleep(0.05)  # waiting for a new recipe from user

    def start_threads(self):
        self.t1 = threading.Thread(target=self.FillMashTankThread, args=[])
        self.t2 = threading.Thread(target=self.FillBoilTankThread, args=[])
        self.t1.daemon = True
        self.t2.daemon = True
        self.t1.start()
        self.t2.start()
