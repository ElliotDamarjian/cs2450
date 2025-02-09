import unittest
from uvsim import UVSim

class TestUVSim(unittest.TestCase):

    def setUp(self):
        self.sim = UVSim()

    # I/O Tests
    def test_read_valid_input(self):
        self.sim.memory[5] = 0
        self.sim.memory[0] = 1005  # READ 05
        
        # Simulating input directly by modifying the method in the class
        self.sim.get_input = lambda: '1234'  # Mock input value directly
        
        
        self.sim.execute()
        self.assertEqual(self.sim.memory[5], 1234)

    def test_read_invalid_input(self):
        self.sim.memory[0] = 1005
        self.sim.get_input = lambda: 'abc'  # Simulate invalid input directly
        
        with self.assertRaises(ValueError):
            self.sim.execute()

    def test_write_output(self):
        self.sim.memory[10] = 5678
        self.sim.memory[0] = 1110
        
        # Capture print output by redirecting stdout
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.sim.execute()
        
        sys.stdout = sys.__stdout__  # Restore original stdout
        
        self.assertIn("Output: 5678", captured_output.getvalue())

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
        
        # Capture print output by redirecting stdout
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.sim.execute()
        
        sys.stdout = sys.__stdout__  # Restore original stdout
        
        self.assertIn("Error: Division by zero", captured_output.getvalue())

    # Control Tests
    def test_branch_valid(self):
        self.sim.memory[0] = 4020  # BRANCH 20
        self.sim.execute()
        self.assertEqual(self.sim.program_counter, 20)

    def test_halt_execution(self):
        self.sim.memory[0] = 4300  # HALT
        self.sim.memory[1] = 1110  # This should not execute
        
        # Capture print output for halting
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.sim.execute()
        
        sys.stdout = sys.__stdout__  # Restore original stdout
        
        self.assertIn("*** Program terminated normally ***", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()
