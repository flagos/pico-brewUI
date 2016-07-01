from future import standard_library
standard_library.install_aliases()
from builtins import object
import unittest
import MashTank
import queue
import time


class Fake_HotTank(object):
    """Fake class to test MashTank """

    def __init__(self, pop_volume_queue):
        self.pop_volume_queue=pop_volume_queue
        pass

    def pop_volume(self, vol):
        self.pop_volume_queue.put(vol)
        pass

class Fake_BoilTank(object):
    """Fake class to test MashTank """
    def __init__(self, start_heat_queue, start_counting_queue):
        self.start_heat_queue     = start_heat_queue
        self.start_counting_queue = start_counting_queue

class Fake_Pico(object):

    def __init__(self):
        self.recipes = []

class Fake_Recipe(object):

    def __init__(self):
        self.mash_steps = []


class MashTankTest(unittest.TestCase):

    def setUp(self):
        self.input_queue          = queue.Queue()
        self.output_queue         = queue.Queue()
        self.volume_queue         = queue.Queue()
        self.start_counting_queue = queue.Queue()
        self.start_heat_queue     = queue.Queue()
        self.start_mash_queue     = queue.Queue()
        self.need_cleaning_queue  = queue.Queue()
        self.pico                 = Fake_Pico()
        self.mashtank = MashTank.MashTank(Fake_HotTank(self.volume_queue), Fake_BoilTank(self.start_heat_queue, self.start_counting_queue), self.start_mash_queue, self.need_cleaning_queue, 0.01, self.input_queue, self.output_queue)
        self.mashtank.start()


    def test_recipe_with_one_step(self):
        recipe = Fake_Recipe()
        recipe.mash_steps.append({'temperature':68, 'duration':0.1, 'name':"saccharification", 'water_volume':20})
        self.pico.recipes.append(recipe)

        self.need_cleaning_queue.get()
        self.need_cleaning_queue.task_done()

        self.assertTrue(self.mashtank.SetPoint is None)

        self.start_mash_queue.put(None)

        self.assertEqual(self.volume_queue.get(), 20) # ok for volume

        self.input_queue.put(66)
        self.input_queue.put(66)
        start = time.time()
        self.input_queue.put(67)
        time.sleep(0.1)
        self.assertFalse(self.mashtank.is_over()) # start at the rigth moment

        self.start_counting_queue.get() # launch boil counting

        self.start_mash_queue.join()
        self.assertTrue(self.mashtank.SetPoint is None)


    def test_recipe_with_three_step(self):
        self.mashtank.push_steps({'temperature':68, 'duration':0.1, 'name':"saccharification", 'water_volume':20})
        self.mashtank.push_steps({'temperature':78, 'duration':0.1, 'name':"mashout", 'water_volume':0, 'dump':True})
        self.mashtank.push_steps({'temperature':68, 'duration':0.1, 'name':"second_run", 'water_volume':10, 'dump':True})

        self.need_cleaning_queue.get()
        self.need_cleaning_queue.task_done()

        self.start_mash_queue.put(None)

        self.assertEqual(self.volume_queue.get(), 20) # ok for volume

        # first step
        self.input_queue.put(66)
        self.input_queue.put(66)
        start = time.time()
        self.input_queue.put(69)
        time.sleep(0.1)
        self.assertFalse(self.mashtank.is_over()) # start at the rigth moment

        # second step
        self.input_queue.put(76)
        self.input_queue.put(76)
        self.input_queue.put(78)
        self.start_heat_queue.get()
        self.start_heat_queue.task_done()

        # third step
        self.assertEqual(self.volume_queue.get(), 10) # ok for volume
        self.input_queue.put(66)
        self.input_queue.put(66)
        self.input_queue.put(69)

        assert self.start_heat_queue.empty() is True

        self.start_counting_queue.get()
        self.start_mash_queue.join()



    def test_two_recipe(self):
        self.test_recipe_with_one_step()
        self.test_recipe_with_three_step()
        pass


    def test_withdumps(self):
        # TBD
        pass

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
