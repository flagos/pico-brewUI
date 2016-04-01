import unittest
import time
from Tank import Chrono

TIMING_PRECISION = 0.1

class ChronoTest(unittest.TestCase):

    def setUp(self):
        self.chrono = Chrono()


    def test_no_pause(self):
        """Test chono with no pause"""

        duration = 2
        self.chrono.launch_chrono(duration)
        assert self.chrono.is_over() == False

        time.sleep(duration - TIMING_PRECISION)
        assert self.chrono.is_over() == False

        time.sleep(2*TIMING_PRECISION)
        assert self.chrono.is_over() == True


    def test_pause_resume(self):
        """ Test with pause/resume"""

        duration = 2
        self.chrono.launch_chrono(duration)
        assert self.chrono.is_over() == False

        self.chrono.pause()
        assert self.chrono.is_over() == False

        time.sleep(2*duration)
        assert self.chrono.is_over() == False

        self.chrono.resume()
        assert self.chrono.is_over() == False

        time.sleep(duration - TIMING_PRECISION)
        assert self.chrono.is_over() == False

        time.sleep(2*TIMING_PRECISION)
        assert self.chrono.is_over() == True



if __name__ == '__main__':
    unittest.main()  # pragma: no cover
