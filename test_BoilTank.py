import unittest
import BoilTank
import Queue
import time


class HotBoilTest(unittest.TestCase):

    def setUp(self, saturation=50):
        self.start_heat_queue  = Queue.Queue()
        self.start_boil_queue = Queue.Queue()
        self.input_test_queue = Queue.Queue()
        self.boiltank = BoilTank.BoilTank(self.start_heat_queue, self.start_boil_queue, 0.01, self.input_test_queue)
        self.boiltank.start()

        pass

    def test_with_one_step(self):
        bk = self.boiltank
        self.assertTrue(bk.consign is None)

        time.sleep(bk.period*5)
        bk.need_cleaning = False

        bk.add_boil_step(95, 0.2)
        self.assertTrue(bk.consign is None) # not heating

        self.start_heat_queue.put(None)  # start heating
        self.start_heat_queue.join() # blocking -- heat should be started
        self.assertEqual(bk.consign, 95) # heating ok

        for i in [80, 85, 90, 92]:
            self.input_test_queue.put(i)

        self.start_boil_queue.put(None) # launching steps

        self.input_test_queue.join() # blocking
        self.assertEqual(bk.start_time, 0)

        self.input_test_queue.put(94)
        self.input_test_queue.join() # blocking
        time.sleep(bk.period)      # time to update start_time variable
        self.assertNotEqual(bk.start_time, 0)

        bk.need_cleaning = False

        self.start_boil_queue.join() # blocking
        self.assertTrue(bk.stop_time - bk.start_time > 0.2)
        self.assertTrue(bk.stop_time - bk.start_time < 0.2 + bk.period)
        pass


    def test_wait_for_cleaning(self):
        bk = self.boiltank
        self.assertTrue(bk.consign is None)

        bk.add_boil_step(95, 0.2)
        self.assertTrue(bk.consign is None) # not heating



        self.start_heat_queue.put(None)  # no start heating -- not cleaned

        time.sleep(bk.period*5)
        assert self.start_heat_queue.empty() is False  # we are not heating

        bk.need_cleaning = False

        self.start_heat_queue.join() # blocking -- heat should be started
        self.assertEqual(bk.consign, 95) # heating ok

        for i in [80, 85, 90, 92]:
            self.input_test_queue.put(i)

        self.start_boil_queue.put(None) # launching steps

        self.input_test_queue.join() # blocking
        self.assertEqual(bk.start_time, 0)

        self.input_test_queue.put(94)
        self.input_test_queue.join() # blocking
        time.sleep(bk.period)      # time to update start_time variable
        self.assertNotEqual(bk.start_time, 0)

        time.sleep(bk.period*5)
        assert self.start_boil_queue.unfinished_tasks != 0  # we have to wait for cleaning

        bk.need_cleaning = False

        self.start_boil_queue.join() # blocking
        self.assertTrue(bk.stop_time - bk.start_time > 0.2)
        self.assertTrue(bk.stop_time - bk.start_time < 0.2 + bk.period)

        pass

    def tearDown(self):
        self.boiltank._Thread__stop()

unittest.main()
