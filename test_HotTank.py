import unittest
import HotTank
import Queue


class HotTankTest(unittest.TestCase):

    def setUp(self, saturation=50):
        self.input_queue  = Queue.Queue()
        self.output_queue = Queue.Queue()
        self.hottank = HotTank.HotTank(saturation, 0.01, self.input_queue, self.output_queue)
        self.hottank.start()

    def run_test(self, orders, temperatures, expected):
        while(expected):
            if orders:
                self.hottank.push_volume(orders.pop(0))

            if temperatures:
                self.input_queue.put(temperatures.pop(0))
            self.assertEqual(self.output_queue.get(), expected.pop(0))


    def test_fill_11_liters(self):
        """Test with a generic pattern of 11 liters."""
        orders = [11]
        temperatures = [55, 55]
        expected = [10, 11]
        self.run_test(orders, temperatures, expected)


    def test_fill_15_liters(self):
        """Test with a generic pattern of 15 liters."""
        orders = [15]
        temperatures = [55, 55, 55, 55, 55, 55, 55, 55]
        expected     = [10, 11, 12, 13, 14, 15, 15, 15]
        self.run_test(orders, temperatures, expected)

    def test_saturation(self):
        """Test with saturation of 15 liters."""
        self.tearDown()
        self.setUp(15)
        orders = [16]
        temperatures = [55, 55, 55, 55, 55, 55, 55, 55]
        expected     = [10, 11, 12, 13, 14, 15, 15, 15]
        self.run_test(orders, temperatures, expected)



    def tearDown(self):
        self.hottank._Thread__stop()





unittest.main()
