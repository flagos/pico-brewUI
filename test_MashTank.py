import unittest
import MashTank
import Queue
import time


class Fake_HotTank:
    """Fake class to test MashTank """

    def __init__(self, pop_volume_queue):
        self.pop_volume_queue=pop_volume_queue
        pass

    def pop_volume(self, vol):
        self.pop_volume_queue.put(vol)
        pass

class Fake_BoilTank:
    """Fake class to test MashTank """
    def __init__(self, input_queue):
        self.input_queue = input_queue

    def is_ready(self):
        return self.input_queue.get()




class MashTankTest(unittest.TestCase):

    def setUp(self):
        self.input_queue  = Queue.Queue()
        self.output_queue = Queue.Queue()
        self.volume_queue = Queue.Queue()
        self.boil_queue   = Queue.Queue()
        self.mashtank = MashTank.MashTank(Fake_HotTank(self.volume_queue), Fake_BoilTank(self.boil_queue), 0.01, self.input_queue, self.output_queue)
        self.mashtank.start()


    def test_recipe_with_one_step(self):
        self.assertTrue(self.mashtank.stop_time == 0)
        self.mashtank.add_mash_step(68, 0.1, "saccharification", 20)
        self.mashtank.need_cleaning = False
        self.mashtank.start_mash()

        self.assertEqual(self.volume_queue.get(), 20) # ok for volume

        self.input_queue.put(66)
        self.input_queue.put(66)
        start = time.time()
        self.input_queue.put(67)
        time.sleep(0.1)
        self.assertTrue(start < self.mashtank.start_time) # start at the rigth moment

        time.sleep(0.1 + 0.01) # wait for step to be completed
        self.assertTrue(self.mashtank.stop_time < time.time())
        self.assertTrue(self.mashtank.stop_time > start + 0.1)

        self.boil_queue.put(True)

    def test_recipe_with_three_step(self):
        self.assertTrue(self.mashtank.stop_time == 0)
        self.mashtank.add_mash_step(68, 0.1, "saccharification", 20)
        self.mashtank.add_mash_step(78, 0.1, "mashout", 0)
        self.mashtank.add_mash_step(68, 0.1, "second_run", 10)
        self.mashtank.need_cleaning = False
        self.mashtank.start_mash()

        self.assertEqual(self.volume_queue.get(), 20) # ok for volume

        # first step
        self.input_queue.put(66)
        self.input_queue.put(66)
        start = time.time()
        self.input_queue.put(69)
        time.sleep(0.1)
        self.assertTrue(start < self.mashtank.start_time) # start at the rigth moment

        # second step
        self.input_queue.put(76)
        self.input_queue.put(76)
        self.input_queue.put(78)

        # third step
        self.assertEqual(self.volume_queue.get(), 10) # ok for volume
        self.input_queue.put(66)
        self.input_queue.put(66)
        self.assertTrue(self.mashtank.stop_time==0)
        self.input_queue.put(69)

        time.sleep(0.1 + 0.01) # wait for step to be completed
        self.assertTrue(self.mashtank.stop_time < time.time())

        self.boil_queue.put(False)
        self.boil_queue.put(False)
        self.assertTrue(self.mashtank.tank_in_use==True)
        self.boil_queue.put(True)
        time.sleep(0.1)  # wait for concurrency
        self.assertTrue(self.mashtank.tank_in_use==False)

    def test_two_recipe(self):
        self.test_recipe_with_one_step()
        while (self.mashtank.tank_in_use):
            pass
        self.test_recipe_with_three_step()
        pass


    def tearDown(self):
        self.mashtank._Thread__stop()


unittest.main()
