import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, colorchooser

class UVSim:
    def __init__(self, root):
        self.memory = [0] * 100
        self.accumulator = 0
        self.instruction_counter = 0
        self.running = True

        # Default theme
        self.primary_color = "#4C721D"  # uvu green
        self.off_color = "#FFFFFF"  

        root.title("UVSim - BasicML Simulator")
        root.geometry("600x550")
        root.configure(bg=self.primary_color)

        # Instruction Input
        self.instruction_label = tk.Label(root, text="Enter BasicML Instructions:", bg=self.primary_color, fg="white")
        self.instruction_label.pack()
        self.instruction_input = scrolledtext.ScrolledText(root, height=5, bg=self.off_color, fg="black")
        self.instruction_input.pack(fill=tk.X, padx=10)

        # Load and Execute buttons
        self.button_frame = tk.Frame(root, bg=self.primary_color)
        self.button_frame.pack(pady=5)
        self.load_button = tk.Button(self.button_frame, text="Load Program", command=self.load_program, bg=self.off_color)
        self.load_button.pack(side=tk.LEFT, padx=5)
        self.execute_button = tk.Button(self.button_frame, text="Execute", command=self.execute_program, bg=self.off_color)
        self.execute_button.pack(side=tk.LEFT, padx=5)
        self.file_button = tk.Button(self.button_frame, text="Load from File", command=self.load_from_file, bg=self.off_color)
        self.file_button.pack(side=tk.LEFT, padx=5)

        # Memory display
        self.memory_label = tk.Label(root, text="Memory:", bg=self.primary_color, fg="white")
        self.memory_label.pack()
        self.memory_listbox = tk.Listbox(root, height=10, bg=self.off_color, fg="black")
        self.memory_listbox.pack(fill=tk.X, padx=10)

        # Accumulator and Instruction Counter Display
        self.status_frame = tk.Frame(root, bg=self.primary_color)
        self.status_frame.pack(pady=5)
        self.accumulator_label = tk.Label(self.status_frame, text=f"Accumulator: {self.accumulator}", bg=self.primary_color, fg="white")
        self.accumulator_label.pack(side=tk.LEFT, padx=10)
        self.instruction_counter_label = tk.Label(self.status_frame, text=f"Instruction Counter: {self.instruction_counter}", bg=self.primary_color, fg="white")
        self.instruction_counter_label.pack(side=tk.LEFT, padx=10)

        # Output display
        self.output_label = tk.Label(root, text="Output:", bg=self.primary_color, fg="white")
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(root, height=5, state=tk.DISABLED, bg=self.off_color, fg="black")
        self.output_text.pack(fill=tk.X, padx=10)

        # Color change button
        self.color_button = tk.Button(root, text="Change Colors", command=self.change_colors, bg=self.off_color)
        self.color_button.pack(pady=5)

        # Help Button
        self.help_button = tk.Button(root, text="Help", command=self.show_help, bg=self.off_color)
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

    def change_colors(self):
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        if primary_color:
            self.primary_color = primary_color

        off_color = colorchooser.askcolor(title="Choose Off Color")[1]
        if off_color:
            self.off_color = off_color

        self.apply_colors()

    def apply_colors(self):
        root.configure(bg=self.primary_color)
        
        self.instruction_label.config(bg=self.primary_color)
        self.memory_label.config(bg=self.primary_color)
        self.output_label.config(bg=self.primary_color)
        self.accumulator_label.config(bg=self.primary_color)
        self.instruction_counter_label.config(bg=self.primary_color)
        self.status_frame.config(bg=self.primary_color)
        self.memory_listbox.config(bg=self.off_color, fg="black")
        self.output_text.config(bg=self.off_color, fg="black")
        self.instruction_input.config(bg=self.off_color, fg="black")
        
        buttons = [self.load_button, self.execute_button, self.file_button, self.color_button, self.help_button]
        for button in buttons:
            button.config(bg=self.off_color, 
                        fg="black",
                        activebackground=self.off_color,
                        highlightbackground=self.off_color,
                        borderwidth=0,
                        highlightthickness=0,
                        relief=tk.FLAT)
            
        self.button_frame.config(bg=self.primary_color)
if __name__ == "__main__":
    root = tk.Tk()
    app = UVSim(root)
    root.mainloop()
