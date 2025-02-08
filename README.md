This is for the unit tests in case we need it.

# Introduction

This test suite verifies the functionality of UVSim, a virtual machine that executes BasicML instructions. It ensures correct handling of I/O, arithmetic, and control operations.

# Prerequisites

Python 3.8 or higher

UVSim module installed or present in the same directory

# Running the Tests

To execute the test suite, run the following command:

python -m unittest test_uvsim.py

# Test Coverage

The test suite includes:

I/O Tests: Ensures correct handling of READ and WRITE instructions.

Arithmetic Tests: Verifies addition and division, including division by zero handling.

Control Tests: Checks branching and halting behavior.

# Troubleshooting

Ensure uvsim.py is correctly implemented and in the same directory.

If ModuleNotFoundError occurs, check the import path for UVSim.

Use python --version to confirm Python 3.8+ is installed.

