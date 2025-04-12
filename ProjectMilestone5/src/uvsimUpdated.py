class UVSim:
    def __init__(self):
        self.memory = [0] * 250  
        self.accumulator = 0     
        self.program_counter = 0 
        self.running = True      
        self.file_format = None  

    def load_program_from_file(self, filename):
        """
        Loads a program from a file into memory.
        Supports both old (4-digit) and new (6-digit) formats.
        Ensures that the file does not exceed 250 instructions and that every
        instruction uses the same number of digits.
        """
        try:
            instruction_count = 0
            detected_format = None  # This will be either 'old' or 'new'
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    # Check for a termination code (adjust as needed)
                    if line == "-99999" or line == "-9999":
                        break

                    # Determine file format from the first valid line
                    if detected_format is None:
                        if len(line) == 4:
                            detected_format = 'old'
                        elif len(line) == 6:
                            detected_format = 'new'
                        else:
                            print("Error: Unrecognized word length. Use either 4-digit or 6-digit words.")
                            return False
                        self.file_format = detected_format  # Save the format for use during execution

                    # Enforce uniform word format across the entire file
                    expected_length = 4 if detected_format == 'old' else 6
                    if len(line) != expected_length:
                        print("Error: Mixed word formats detected. File must consist of only 4-digit or 6-digit words.")
                        return False

                    # Prevent files from having more than 250 commands
                    if instruction_count >= 250:
                        print("Error: File exceeds the maximum program size of 250 lines.")
                        return False

                    try:
                        # Convert the instruction from the file to an integer
                        word = int(line)
                        # Validate the numerical value depending on file format:
                        if detected_format == 'old':
                            if not -9999 <= word <= 9999:
                                print(f"Warning: Invalid number {word} at line {instruction_count+1}. Must be between -9999 and 9999.")
                                continue
                        else:  # new format
                            if not -99999 <= word <= 99999:
                                print(f"Warning: Invalid number {word} at line {instruction_count+1}. Must be between -99999 and 99999.")
                                continue

                        self.memory[instruction_count] = word
                        instruction_count += 1
                    except ValueError:
                        print(f"Error: Invalid instruction format at line {instruction_count + 1}.")
                        return False

            print(f"Loaded {instruction_count} instructions successfully ({detected_format} format).")
            return True

        except FileNotFoundError:
            print(f"Error: Could not find file '{filename}'")
            return False
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return False

    def get_input(self):
        """
        Function for input that can be overridden in tests for easier mock inputs.
        """
        return input("Enter a number: ")

    def execute(self):
        print("\n*** Program execution begins ***")
        while self.running and self.program_counter < 250:
            instruction = self.memory[self.program_counter]

            # Decode opcode and operand based on file format
            if self.file_format == 'old':
                opcode = abs(instruction) // 100   # 2-digit opcode
                operand = abs(instruction) % 100   # 2-digit operand
            elif self.file_format == 'new':
                opcode = abs(instruction) // 1000  # 3-digit opcode (e.g., 010 becomes 10)
                operand = abs(instruction) % 1000  # 3-digit operand
            else:
                print("Error: File format not recognized. Cannot execute program.")
                break

            # Validate operand (memory address should be within 0 to 249)
            if operand < 0 or operand > 249:
                print(f"Error: Invalid memory address {operand}. Must be between 000 and 249.")
                self.running = False
                break

            self.program_counter += 1

            # Process instructions based on opcode
            if opcode == 10:   # READ
                try:
                    value = int(self.get_input())
                    if self.file_format == 'old':
                        if not -9999 <= value <= 9999:
                            raise ValueError("Invalid input: must be a 4-digit number.")
                    else:
                        if not -99999 <= value <= 99999:
                            raise ValueError("Invalid input: must be a 6-digit number.")
                    self.memory[operand] = value
                except ValueError as e:
                    raise ValueError(str(e))

            elif opcode == 11:  # WRITE
                print(f"Output: {self.memory[operand]}")

            elif opcode == 20:  # LOAD
                self.accumulator = self.memory[operand]

            elif opcode == 21:  # STORE
                self.memory[operand] = self.accumulator

            elif opcode == 30:  # ADD
                self.accumulator += self.memory[operand]
                # Check for overflow
                if self.file_format == 'old' and not (-9999 <= self.accumulator <= 9999):
                    print("Overflow error in ADD operation.")
                    self.running = False
                elif self.file_format == 'new' and not (-99999 <= self.accumulator <= 99999):
                    print("Overflow error in ADD operation.")
                    self.running = False

            elif opcode == 31:  # SUBTRACT
                self.accumulator -= self.memory[operand]
                if self.file_format == 'old' and not (-9999 <= self.accumulator <= 9999):
                    print("Overflow error in SUBTRACT operation.")
                    self.running = False
                elif self.file_format == 'new' and not (-99999 <= self.accumulator <= 99999):
                    print("Overflow error in SUBTRACT operation.")
                    self.running = False

            elif opcode == 32:  # DIVIDE
                if self.memory[operand] != 0:
                    self.accumulator //= self.memory[operand]
                else:
                    print("Error: Division by zero.")
                    self.running = False

            elif opcode == 33:  # MULTIPLY
                self.accumulator *= self.memory[operand]
                if self.file_format == 'old' and not (-9999 <= self.accumulator <= 9999):
                    print("Overflow error in MULTIPLY operation.")
                    self.running = False
                elif self.file_format == 'new' and not (-99999 <= self.accumulator <= 99999):
                    print("Overflow error in MULTIPLY operation.")
                    self.running = False

            elif opcode == 40:  # BRANCH
                self.program_counter = operand

            elif opcode == 41:  # BRANCHNEG
                if self.accumulator < 0:
                    self.program_counter = operand

            elif opcode == 42:  # BRANCHZERO
                if self.accumulator == 0:
                    self.program_counter = operand

            elif opcode == 43:  # HALT
                print("*** Program terminated normally ***")
                self.running = False

            else:
                print(f"Error: Invalid opcode {opcode}.")
                self.running = False

        print(f"Final Accumulator Value: {self.accumulator}")

def main():
    while True:
        simulator = UVSim()
        print("Welcome to UVSim!")
        filename = input("Enter the name of the input file: ")

        if simulator.load_program_from_file(filename):
            simulator.execute()

if __name__ == "__main__":
    main()
