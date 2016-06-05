from future import standard_library
standard_library.install_aliases()
import unittest
import BoilTank
import queue
import time


class HotBoilTest(unittest.TestCase):

    def setUp(self, saturation=50):
        self.start_heat_queue     = queue.Queue()
        self.start_boil_queue     = queue.Queue()
        self.start_counting_queue = queue.Queue()
        self.need_cleaning_queue  = queue.Queue()
        self.input_test_queue     = queue.Queue()

        self.boiltank = BoilTank.BoilTank(self.start_heat_queue,
                                          self.start_boil_queue,
                                          self.start_counting_queue,
                                          self.need_cleaning_queue,
                                          .01,
                                          self.input_test_queue)
        self.boiltank.start()

        pass

    def test_with_one_step(self):
        bk = self.boiltank
        self.assertTrue(bk.SetPoint is None)

        bk.add_boil_step(95, 0.2)
        bk.start_boil_queue.put(None)

        self.assertTrue(bk.SetPoint is None)  # not heating


        self.start_heat_queue.put(None)  # start heating
        self.start_heat_queue.join()  # blocking -- heat should be started
        self.assertEqual(bk.SetPoint, 95)  # heating ok

        for i in [80, 85, 90, 92]:
            self.input_test_queue.put(i)

        self.start_counting_queue.put(None)  # launching steps

        self.input_test_queue.join()  # blocking
        self.assertEqual(bk.start_time, 0)

        self.input_test_queue.put(94)
        self.input_test_queue.join()  # blocking
        time.sleep(bk.period)      # time to update start_time variable
        self.assertFalse(bk.is_over())

        bk.need_cleaning_queue.get()
        bk.need_cleaning_queue.task_done()


        self.start_counting_queue.join()  # blocking
        self.start_boil_queue.join()  # blocking

        self.assertTrue(bk.SetPoint is None)

        self.assertTrue(bk.stop_time - bk.start_chrono > 0.2)
        self.assertTrue(bk.stop_time - bk.start_chrono < 0.2 + bk.period)
        pass


    def test_wait_for_cleaning(self):
        bk = self.boiltank
        self.assertTrue(bk.SetPoint is None)

        bk.add_boil_step(95, 0.2)
        self.start_boil_queue.put(None)
        self.assertTrue(bk.SetPoint is None)  # not heating

        self.start_heat_queue.put(None)  # we can start heating -- clean at startup

        self.start_heat_queue.join()  # blocking -- heat should be started
        self.assertEqual(bk.SetPoint, 95)  # heating ok


        for i in [80, 85, 90, 92]:
            self.input_test_queue.put(i)

        self.start_counting_queue.put(None)  # launching steps

        self.input_test_queue.join()  # blocking
        self.assertTrue(bk.is_over())

        self.input_test_queue.put(94)
        self.input_test_queue.join()  # blocking
        self.assertFalse(bk.is_over())

        time.sleep(1)  # wait for all steps to be completed
        assert self.start_boil_queue.unfinished_tasks != 0  # we have to wait for cleaning

        bk.need_cleaning_queue.get()
        bk.need_cleaning_queue.task_done()

        self.start_counting_queue.join()  # blocking
        self.start_boil_queue.join()  # blocking
        self.assertTrue(bk.stop_time - bk.start_chrono > 0.2)
        self.assertTrue(bk.stop_time - bk.start_chrono < 0.2 + bk.period)

        pass


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
