import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

class UVSim:
    def __init__(self, root):
        self.memory = [0] * 100  # Store 100 words
        self.accumulator = 0
        self.instruction_counter = 0
        
        root.title("UVSim - BasicML Simulator")
        root.geometry("600x500")
        
        # Instruction Input
        self.instruction_label = tk.Label(root, text="Enter BasicML Instructions:")
        self.instruction_label.pack()
        self.instruction_input = scrolledtext.ScrolledText(root, height=5)
        self.instruction_input.pack(fill=tk.X, padx=10)
        
        # Load and Execute buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        self.load_button = tk.Button(button_frame, text="Load Program", command=self.load_program)
        self.load_button.pack(side=tk.LEFT, padx=5)
        self.execute_button = tk.Button(button_frame, text="Execute", command=self.execute_program)
        self.execute_button.pack(side=tk.LEFT, padx=5)
        self.file_button = tk.Button(button_frame, text="Load from File", command=self.load_from_file)
        self.file_button.pack(side=tk.LEFT, padx=5)
        
        # Memory display
        self.memory_label = tk.Label(root, text="Memory:")
        self.memory_label.pack()
        self.memory_listbox = tk.Listbox(root, height=10)
        self.memory_listbox.pack(fill=tk.X, padx=10)
        
        # Accumulator and Instruction Counter Display
        self.status_frame = tk.Frame(root)
        self.status_frame.pack(pady=5)
        self.accumulator_label = tk.Label(self.status_frame, text=f"Accumulator: {self.accumulator}")
        self.accumulator_label.pack(side=tk.LEFT, padx=10)
        self.instruction_counter_label = tk.Label(self.status_frame, text=f"Instruction Counter: {self.instruction_counter}")
        self.instruction_counter_label.pack(side=tk.LEFT, padx=10)
        
        # Output display
        self.output_label = tk.Label(root, text="Output:")
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(root, height=5, state=tk.DISABLED)
        self.output_text.pack(fill=tk.X, padx=10)
        
        # Help Button
        self.help_button = tk.Button(root, text="Help", command=self.show_help)
        self.help_button.pack(pady=5)
    
    def load_program(self):
        program = self.instruction_input.get("1.0", tk.END).strip().split("\n")
        self.memory_listbox.delete(0, tk.END)
        for i, instruction in enumerate(program):
            try:
                instruction = int(instruction)
                self.memory[i] = instruction
                self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
            except ValueError:
                messagebox.showerror("Error", "Invalid instruction format. Must be an integer.")
                return
    
    def execute_program(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "Executing program...\n")
        self.output_text.config(state=tk.DISABLED)
        
    def load_from_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.instruction_input.delete("1.0", tk.END)
                self.instruction_input.insert(tk.END, content)
    
    def show_help(self):
        messagebox.showinfo("Help", "BasicML Commands:\n1001 - Read Input\n2001 - Load into Accumulator\n3001 - Add\n3101 - Subtract\n3201 - Divide\n3301 - Multiply\n4300 - Halt")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = UVSim(root)
    root.mainloop()
