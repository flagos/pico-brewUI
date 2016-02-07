import unittest
import Pico
import Queue
import time


class Fake_HotTank:
    """Fake class to test MashTank """

    def __init__(self, push_volume_queue):
        self.push_volume_queue=push_volume_queue
        pass

    def push_volume(self, vol):
        self.push_volume_queue.put(vol)
        pass


class Fake_MashTank:
    """Fake class to test pico"""
    def __init__(self, start_mash_queue, push_mash_steps_queue ):
        self.start_mash_queue      = start_mash_queue
        self.push_mash_steps_queue = push_mash_steps_queue


    def push_steps(self, step):
        self.push_mash_steps_queue.put(step)



class Fake_BoilTank:
    """Fake class to test MashTank """
    def __init__(self, start_boil_queue, push_boil_steps_queue):
        self.start_boil_queue       = start_boil_queue
        self.push_boil_steps_queue = push_boil_steps_queue

    def push_steps(self, step):
        self.push_boil_steps_queue.put(step)

class PicoTest(unittest.TestCase):

    def setUp(self, saturation=50):
        self.push_volume_queue     = Queue.Queue()

        self.start_boil_queue      = Queue.Queue()
        self.push_boil_steps_queue = Queue.Queue()

        self.start_mash_queue      = Queue.Queue()
        self.push_mash_steps_queue = Queue.Queue()

        self.pico = Pico.Pico()
        self.pico.real_init(Fake_HotTank(self.push_volume_queue),
                            Fake_MashTank(self.start_mash_queue, self.push_mash_steps_queue),
                            Fake_BoilTank(self.start_boil_queue, self.push_boil_steps_queue))
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
        volume = self.push_volume_queue.get()
        assert volume == 1.2 * 18.93

        for step in recipe_e["mash_steps"]:
            out = self.push_mash_steps_queue.get()
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
        recipe_e = recipe2_e
        recipe = self.pico.fetch_recipe(recipe_e["url"])
        self.pico.add_recipe(recipe)


        recipe_e = recipe1_e
        volume = self.push_volume_queue.get()
        assert volume == 1.2 * recipe_e["volume"]

        for step in recipe_e["mash_steps"]:
            out = self.push_mash_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"]    == step["duration"]
            assert out["dump"]        == step["dump"]

        for step in recipe_e["boil_steps"]:
            out = self.push_boil_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"] == step["duration"]

        self.start_mash_queue.get()
        self.start_boil_queue.get()


        recipe_e = recipe2_e
        volume = self.push_volume_queue.get()
        assert volume == 1.2 * recipe_e["volume"]

        assert self.push_mash_steps_queue.empty() is True
        self.start_mash_queue.task_done()

        for step in recipe_e["mash_steps"]:
            out = self.push_mash_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"]    == step["duration"]
            assert out["dump"]        == step["dump"]

        assert self.push_boil_steps_queue.empty() is True
        self.start_boil_queue.task_done()


        for step in recipe_e["boil_steps"]:
            out = self.push_boil_steps_queue.get()
            assert out["temperature"] == step["temperature"]
            assert out["duration"] == step["duration"]

        self.start_mash_queue.get()
        self.start_mash_queue.task_done()

        self.start_boil_queue.get()
        self.start_boil_queue.task_done()





    def tearDown(self):
        self.pico.run_thread = False


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
