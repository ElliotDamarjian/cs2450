import unittest
from uvsim import UVSim

class TestUVSim(unittest.TestCase):

    def setUp(self):
        self.sim = UVSim()

    # I/O Tests
    def test_read_valid_input(self):
        self.sim.memory[5] = 0
        self.sim.memory[0] = 1005  # READ 05
        self.sim.get_input = lambda: 1234
        self.sim.execute()
        self.assertEqual(self.sim.memory[5], 1234)

    def test_read_invalid_input(self):
        self.sim.memory[0] = 1005
        self.sim.get_input = lambda: "abc"
        with self.assertRaises(ValueError):
            self.sim.execute()

    def test_write_output(self):
        self.sim.memory[10] = 5678
        self.sim.memory[0] = 1110
        with self.assertLogs() as captured:
            self.sim.execute()
        self.assertIn("5678", captured.output[0])

    # Arithmetic Tests
    def test_addition_valid(self):
        self.sim.accumulator = 10
        self.sim.memory[5] = 15
        self.sim.memory[0] = 3005
        self.sim.execute()
        self.assertEqual(self.sim.accumulator, 25)

    def test_divide_by_zero(self):
        self.sim.accumulator = 10
        self.sim.memory[5] = 0
        self.sim.memory[0] = 3205
        with self.assertRaises(ZeroDivisionError):
            self.sim.execute()

    # Control Tests
    def test_branch_valid(self):
        self.sim.memory[0] = 4020  # BRANCH 20
        self.sim.execute()
        self.assertEqual(self.sim.pc, 20)

    def test_halt_execution(self):
        self.sim.memory[0] = 4300  # HALT
        self.sim.memory[1] = 1110  # This should not execute
        with self.assertLogs() as captured:
            self.sim.execute()
        self.assertEqual(len(captured.output), 0)

if __name__ == "__main__":
    unittest.main()
