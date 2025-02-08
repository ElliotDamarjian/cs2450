class UVSim:
    def __init__(self):
        self.memory = [0] * 100  # Creates a list of 100-word memory
        self.accumulator = 0     # Register for arithmetic operations
        self.program_counter = 0 # Keeps track of current instruction
        self.running = True      # Controls program execution

    def load_program_from_file(self, filename):
        try:
            instruction_count = 0
            with open(filename, 'r') as file:   # Opens file in read mode
                for line in file:               # Reads file line by line
                    line = line.strip()         # Removes whitespace/newlines
                    if not line:                # Skips empty lines
                        continue
                        
                    if line == "-99999":        # Stop if we hit -99999
                        break
                        
                    try:
                        word = int(line)                                            # Converts string to integer
                        if -9999 <= word <= 9999:                                   # Validates number range
                            self.memory[instruction_count] = word                   # Stores in memory
                            instruction_count += 1
                            if instruction_count >= 100:                            # Checks memory limit
                                print("Warning: Program exceeds memory size.")
                                break
                        else:
                            print(f"Warning: Invalid number {word} at line {instruction_count + 1}. Must be between -9999 and +9999")
                    except ValueError:
                        print(f"Warning: Invalid instruction format at line {instruction_count + 1}")
                        
            print(f"Loaded {instruction_count} instructions successfully.")
            return True
            
        except FileNotFoundError:
            print(f"Error: Could not find file '{filename}'")
            return False
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return False

    def execute(self):
        print("\n*** Program execution begins ***")
        while self.running and self.program_counter < 100:
            instruction = self.memory[self.program_counter]
            opcode = abs(instruction) // 100
            operand = abs(instruction) % 100
            
            self.program_counter += 1

            if opcode == 10:   # READ
                try:
                    value = int(input("Enter a number: "))
                    if -9999 <= value <= 9999:
                        self.memory[operand] = value
                    else:
                        print("Error: Number must be between -9999 and +9999")
                except ValueError:
                    print("Error: Please enter a valid number")
                    
            elif opcode == 11:  # WRITE
                print(f"Output: {self.memory[operand]}")
                
            elif opcode == 20:  # LOAD
                self.accumulator = self.memory[operand]
                
            elif opcode == 21:  # STORE
                self.memory[operand] = self.accumulator
                
            elif opcode == 30:  # ADD
                self.accumulator += self.memory[operand]
                
            elif opcode == 31:  # SUBTRACT
                self.accumulator -= self.memory[operand]
                
            elif opcode == 32:  # DIVIDE
                if self.memory[operand] != 0:
                    self.accumulator //= self.memory[operand]
                else:
                    print("Error: Division by zero")
                    self.running = False
                    
            elif opcode == 33:  # MULTIPLY
                self.accumulator *= self.memory[operand]
                
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
                print(f"Error: Invalid opcode {opcode}")
                self.running = False

def main():
    while True:
        simulator = UVSim()
        print("Welcome to UVSim!")
        
        filename = input("Enter the name of the input file: ")
            
        if simulator.load_program_from_file(filename):
            simulator.execute()
        

if __name__ == "__main__":
    main()
