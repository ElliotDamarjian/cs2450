# **Installation**
Ensure you have Python Version 3 or later is installed.

Install Tkinter if it's not already included in your Python distribution with ```pip install tk ```

# **Running the Application**
Navigate to the project folder.


Open and Run ```GUI.py```

The graphical user interface will open.

Double check the appropriate files are in the correct location.
# Using the GUI

Entering Instructions Manually

Click on the Instruction Input Field.

Enter a series of four-digit BasicML instructions. Each on separate lines (e.g., +1007 for READ).

Click "Load Program" to add it to memory.

Click "Execute" button to run the instructions.

# Uploading a Program File
Click the "Load from File" to open a file dialog.

Select a .txt file containing BasicML instructions.

The instructions will be loaded into memory.

Click the "Execute" to run the loaded program.

# Viewing Outputs
Output from WRITE operations appears in a designated output box.
Errors or invalid commands will display an error message.


# Help Button
The Help button at the bottom of the GUI opens a popup displaying a list of supported opcode commands and their descriptions.

### Supported Opcodes
<pre>
Opcode | Instruction  | Description

10XX	 READ           Reads a number from user input and stores it in memory at XX.
    
11XX	 WRITE          Writes the value from memory location XX to the output.

20XX	 LOAD           Loads the value from memory XX into the accumulator.

21XX	 STORE          Stores the accumulator value into memory XX.

30XX	 ADD            Adds the value at memory XX to the accumulator.
    
31XX	 SUBTRACT       Subtracts the value at memory XX from the accumulator.

32XX	 DIVIDE	        Divides the accumulator by the value at memory XX.

33XX	 MULTIPLY       Multiplies the accumulator by the value at memory XX.
    
40XX	 BRANCH	        Jumps execution to memory location XX.

41XX	 BRANCHNEG      Jumps to XX if the accumulator is negative.

42XX	 BRANCHZERO     Jumps to XX if the accumulator is zero.

4300	 HALT	        Stops execution.
</pre>

<h5> *Disclaimer - Program not entirely integrated* </h5>
