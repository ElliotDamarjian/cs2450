import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, colorchooser

class UVSim:
    def __init__(self, root):
        self.memory = []
        self.accumulator = 0
        self.instruction_counter = 0

        # Default theme
        self.primary_color = "#4C721D"  # UVU Green
        self.off_color = "#FFFFFF"

        root.title("UVSim - BasicML Simulator")
        root.geometry("700x600")
        root.configure(bg=self.primary_color)

        self.create_widgets(root)

    def create_widgets(self, root):
        """Creates all GUI widgets."""
        # Instruction Input
        self.instruction_label = tk.Label(root, text="Enter a BasicML Command:", bg=self.primary_color, fg="white")
        self.instruction_label.pack()

        self.command_input = tk.Entry(root, width=50, bg=self.off_color, fg="black")
        self.command_input.pack(pady=5)

        self.add_command_button = tk.Button(root, text="Add to Memory", command=self.add_command, bg=self.off_color)
        self.add_command_button.pack()

        # Memory Display
        self.memory_label = tk.Label(root, text="Memory:", bg=self.primary_color, fg="white")
        self.memory_label.pack()

        self.memory_listbox = tk.Listbox(root, height=10, bg=self.off_color, fg="black")
        self.memory_listbox.pack(fill=tk.X, padx=10, pady=5)

        # Control Buttons
        self.button_frame = tk.Frame(root, bg=self.primary_color)
        self.button_frame.pack(pady=5)

        self.load_button = tk.Button(self.button_frame, text="Load Program", command=self.load_program, bg=self.off_color)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.execute_button = tk.Button(self.button_frame, text="Execute", command=self.execute_program, bg=self.off_color)
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.file_button = tk.Button(self.button_frame, text="Load from File", command=self.load_from_file, bg=self.off_color)
        self.file_button.pack(side=tk.LEFT, padx=5)

        # Accumulator & Instruction Counter Display
        self.status_frame = tk.Frame(root, bg=self.primary_color)
        self.status_frame.pack(pady=5)

        self.accumulator_label = tk.Label(self.status_frame, text=f"Accumulator: {self.accumulator}", bg=self.primary_color, fg="white")
        self.accumulator_label.pack(side=tk.LEFT, padx=10)

        self.instruction_counter_label = tk.Label(self.status_frame, text=f"Instruction Counter: {self.instruction_counter}", bg=self.primary_color, fg="white")
        self.instruction_counter_label.pack(side=tk.LEFT, padx=10)

        # Enlarged Output Display
        self.output_label = tk.Label(root, text="Output:", bg=self.primary_color, fg="white")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(root, height=10, state=tk.DISABLED, bg=self.off_color, fg="black")
        self.output_text.pack(fill=tk.X, padx=10, pady=5)

        # Help & Color Change Buttons
        self.color_button = tk.Button(root, text="Change Colors", command=self.change_colors, bg=self.off_color)
        self.color_button.pack(pady=5)

        self.help_button = tk.Button(root, text="Help", command=self.show_help, bg=self.off_color)
        self.help_button.pack(pady=5)

    def add_command(self):
        """Adds an individual command to memory."""
        command = self.command_input.get().strip()
        if command:
            try:
                instruction = int(command)
                index = len(self.memory)
                self.memory.append(instruction)
                self.memory_listbox.insert(tk.END, f"{index}: {instruction}")
                self.command_input.delete(0, tk.END)  # Clear input field
            except ValueError:
                messagebox.showerror("Error", "Invalid command. Must be an integer.")

    def load_program(self):
        """Loads the instructions from memory."""
        if not self.memory:
            messagebox.showerror("Error", "No commands in memory to load.")
            return

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "Program loaded into memory.\n")
        self.output_text.config(state=tk.DISABLED)

    def execute_program(self):
        """Runs the loaded program and updates output."""
        if not self.memory:
            messagebox.showerror("Error", "No program loaded. Please add commands to memory first.")
            return

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "Executing program...\n")

        # Simulating execution logic (modify for real execution)
        for instruction in self.memory:
            self.output_text.insert(tk.END, f"Executing: {instruction}\n")

        self.output_text.insert(tk.END, f"Execution complete.\nAccumulator: {self.accumulator}\n")
        self.output_text.config(state=tk.DISABLED)

    def load_from_file(self):
        """Loads a program from a file into memory."""
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read().splitlines()
                self.memory_listbox.delete(0, tk.END)
                self.memory.clear()

                for line in content:
                    try:
                        instruction = int(line)
                        index = len(self.memory)
                        self.memory.append(instruction)
                        self.memory_listbox.insert(tk.END, f"{index}: {instruction}")
                    except ValueError:
                        messagebox.showerror("Error", "Invalid instruction format in file.")
                        return

    def show_help(self):
        """Displays help information."""
        messagebox.showinfo("Help", "BasicML Commands:\n1001 - Read Input\n2001 - Load into Accumulator\n3001 - Add\n3101 - Subtract\n3201 - Divide\n3301 - Multiply\n4300 - Halt")

    def change_colors(self):
        """Changes the primary and off colors."""
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        if primary_color:
            self.primary_color = primary_color

        off_color = colorchooser.askcolor(title="Choose Off Color")[1]
        if off_color:
            self.off_color = off_color

        self.apply_colors()

    def apply_colors(self):
        """Applies color changes throughout the GUI."""
        root.configure(bg=self.primary_color)

        self.instruction_label.config(bg=self.primary_color)
        self.memory_label.config(bg=self.primary_color)
        self.output_label.config(bg=self.primary_color)
        self.accumulator_label.config(bg=self.primary_color)
        self.instruction_counter_label.config(bg=self.primary_color)
        self.status_frame.config(bg=self.primary_color)
        self.memory_listbox.config(bg=self.off_color, fg="black")
        self.output_text.config(bg=self.off_color, fg="black")
        self.command_input.config(bg=self.off_color, fg="black")

        buttons = [self.load_button, self.execute_button, self.file_button, self.color_button, self.help_button, self.add_command_button]
        for button in buttons:
            button.config(bg=self.off_color, fg="black")

        self.button_frame.config(bg=self.primary_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSim(root)
    root.mainloop()
