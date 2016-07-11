from future import standard_library
standard_library.install_aliases()
from builtins import object
import unittest
import Pico
import queue
import time


class Fake_HotTank(object):
    """Fake class to test MashTank """

    def __init__(self, push_volume_queue):
        self.push_volume_queue=push_volume_queue
        pass

    def push_volume(self, vol):
        self.push_volume_queue.put(vol)
        pass


class Fake_MashTank(object):
    """Fake class to test pico"""
    def __init__(self, need_cleaning_queue, start_mash_queue):
        self.need_cleaning_queue   = need_cleaning_queue
        self.start_mash_queue      = start_mash_queue
        self.recipe_index          = 0

    def set_pico(self, pico):
        self.pico = pico


class Fake_BoilTank(object):
    """Fake class to test MashTank """
    def __init__(self, need_cleaning_queue, start_boil_queue, push_boil_steps_queue):
        self.start_boil_queue       = start_boil_queue
        self.push_boil_steps_queue = push_boil_steps_queue
        self.need_cleaning_queue   = need_cleaning_queue
        

    def push_steps(self, step):
        self.push_boil_steps_queue.put(step)
        
    def set_pico(self, pico):
        self.pico = pico

class PicoTest(unittest.TestCase):

    def setUp(self, saturation=50):
        self.push_volume_queue     = queue.Queue()

        self.need_cleaning_queue   = queue.Queue()
        self.start_boil_queue      = queue.Queue()
        self.push_boil_steps_queue = queue.Queue()

        self.start_mash_queue      = queue.Queue()

        self.pico = Pico.Pico()
        self.pico.real_init(Fake_HotTank(self.push_volume_queue),
                            Fake_MashTank(self.need_cleaning_queue, self.start_mash_queue),
                            Fake_BoilTank(queue.Queue(), self.start_boil_queue, self.push_boil_steps_queue),
                            None)
        pass

    def test_one_recipe(self):
        recipe_e = {
            "url": "https://www.brewtoad.com/recipes/geronimo-3",
            "mash_steps": [
                {"temperature": 68, "duration":90, "dump":False},
                {"temperature": 78, "duration":10, "dump":True},
                {"temperature": 78, "duration":10, "dump":True}
                ],
            "boil_steps": [
                {"duration":60, "temperature":98}
                ]
        }

        self.pico.start_threads()
        recipe = self.pico.fetch_recipe(recipe_e["url"])
        self.pico.add_recipe(recipe)

        self.pico.mashtank.need_cleaning_queue.put(None)
        time.sleep(1)
        self.pico.update_task(recipe.mash_task_id, "true")  # should be done by user on UI
        self.pico.mashtank.need_cleaning_queue.join()
        
        
        volume = self.push_volume_queue.get()
        assert volume == 1.2 * 18.93

        for idx, step in enumerate(recipe_e["mash_steps"]):
            out = self.pico.recipes[self.pico.mashtank.recipe_index].mash_steps[idx]
            assert out["temperature"] == step["temperature"]
            assert out["duration"]    == step["duration"]
            assert out["dump"]        == step["dump"]


        for step in recipe_e["boil_steps"]:
            out = self.push_boil_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"] == step["duration"]

        self.start_mash_queue.get()
        self.start_mash_queue.task_done()
        
        self.start_boil_queue.get()
        self.start_boil_queue.task_done()

        self.pico.boiltank.need_cleaning_queue.put(None)
        time.sleep(1)
        self.pico.update_task(recipe.boil_task_id, "true")  # should be done by user on UI
        self.pico.boiltank.need_cleaning_queue.join()
        

    def test_2_recipes(self):
        recipe1_e = {
            "url": "https://www.brewtoad.com/recipes/geronimo-3",
            "volume": 18.93,
            "mash_steps": [
                {"temperature": 68, "duration":90, "dump":False},
                {"temperature": 78, "duration":10, "dump":True},
                {"temperature": 78, "duration":10, "dump":True}
                ],
            "boil_steps": [
                {"duration":60, "temperature":98}
                ]
        }

        recipe2_e = {
            "url": "https://www.brewtoad.com/recipes/squirrels-brewery",
            "volume": 18.93,
            "mash_steps": [
                {"temperature": 68, "duration":60, "dump":False},
                {"temperature": 78, "duration":10, "dump":True},
                {"temperature": 78, "duration":10, "dump":True}
                ],
            "boil_steps": [
                {"duration":60, "temperature":98}
                ]
        }


        self.pico.start_threads()
        recipe_e = recipe1_e
        recipe = self.pico.fetch_recipe(recipe_e["url"])
        self.pico.add_recipe(recipe)

        # add malt 
        self.pico.mashtank.need_cleaning_queue.put(None)
        time.sleep(1)
        self.pico.update_task(recipe.mash_task_id, "true")  # should be done by user on UI
        self.pico.mashtank.need_cleaning_queue.join()


        recipe_e = recipe2_e
        recipe = self.pico.fetch_recipe(recipe_e["url"])
        self.pico.add_recipe(recipe)

        recipe_e = recipe1_e
        volume = self.push_volume_queue.get()
        assert volume == 1.2 * recipe_e["volume"]  # check drive hot tank

        for idx, step in enumerate(recipe_e["mash_steps"]):  # check mash tank programmation
            out = self.pico.recipes[self.pico.mashtank.recipe_index].mash_steps[idx]
            assert out["temperature"] == step["temperature"]
            assert out["duration"]    == step["duration"]
            assert out["dump"]        == step["dump"]

        for step in recipe_e["boil_steps"]:  # check boil tank drive
            out = self.push_boil_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"] == step["duration"]

        self.start_mash_queue.get()  # check launch tanks
        self.start_boil_queue.get()


        recipe_e = recipe2_e
        volume = self.push_volume_queue.get()
        assert volume == 1.2 * recipe_e["volume"]

        self.start_mash_queue.task_done()

        self.pico.mashtank.need_cleaning_queue.put(None)
        time.sleep(1)
        self.pico.update_task(recipe.mash_task_id, "true")  # should be done by user on UI
        self.pico.mashtank.need_cleaning_queue.join()

        
        for idx, step in enumerate(recipe_e["mash_steps"]):
            out = self.pico.recipes[self.pico.mashtank.recipe_index].mash_steps[idx]
            assert out["temperature"] == step["temperature"]
            assert out["duration"]    == step["duration"]
            assert out["dump"]        == step["dump"]

        assert self.push_boil_steps_queue.empty() is True
        self.start_boil_queue.task_done()

        self.pico.boiltank.need_cleaning_queue.put(None)
        time.sleep(1)
        self.pico.update_task(self.pico.recipes[0].boil_task_id, "true")  # should be done by user on UI
        self.pico.boiltank.need_cleaning_queue.join()
        

        for step in recipe_e["boil_steps"]:
            out = self.push_boil_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"] == step["duration"]

        self.start_mash_queue.get()
        self.start_mash_queue.task_done()

        self.start_boil_queue.get()
        self.start_boil_queue.task_done()

        self.pico.boiltank.need_cleaning_queue.put(None)
        time.sleep(1)
        self.pico.update_task(self.pico.recipes[1].boil_task_id, "true")  # should be done by user on UI
        self.pico.boiltank.need_cleaning_queue.join()
        
        


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
