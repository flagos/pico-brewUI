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
    def __init__(self, start_heat_queue, start_counting_queue):
        self.start_heat_queue     = start_heat_queue
        self.start_counting_queue = start_counting_queue


class MashTankTest(unittest.TestCase):

    def setUp(self):
        self.input_queue          = Queue.Queue()
        self.output_queue         = Queue.Queue()
        self.volume_queue         = Queue.Queue()
        self.start_counting_queue = Queue.Queue()
        self.start_heat_queue     = Queue.Queue()
        self.start_mash_queue     = Queue.Queue()
        self.need_cleaning_queue  = Queue.Queue()
        self.mashtank = MashTank.MashTank(Fake_HotTank(self.volume_queue), Fake_BoilTank(self.start_heat_queue, self.start_counting_queue), self.start_mash_queue, self.need_cleaning_queue, 0.01, self.input_queue, self.output_queue)
        self.mashtank.start()


    def test_recipe_with_one_step(self):
        self.mashtank.add_mash_step(68, 0.1, "saccharification", 20)

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
        self.mashtank.add_mash_step(68, 0.1, "saccharification", 20)
        self.mashtank.add_mash_step(78, 0.1, "mashout", 0, True)
        self.mashtank.add_mash_step(68, 0.1, "second_run", 10, True)

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

    def tearDown(self):
        self.mashtank._Thread__stop()


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
