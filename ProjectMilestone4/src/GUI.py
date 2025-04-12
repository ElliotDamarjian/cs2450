import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, colorchooser
from UVSim import UVSim as UVSimBackend  # Import the UVSim class

class UVSim:
    def __init__(self, root):
        self.simulator = UVSimBackend()  # Initialize UVSim backend
        self.memory = []
        self.accumulator = 0
        self.instruction_counter = 0
        self.last_directory = ""
        self.file_format = None  # Track file format ('old' or 'new')
        self.clipboard = None

        # Default theme
        self.primary_color = "#4C721D"  # UVU Green
        self.off_color = "#FFFFFF"

        root.title("UVSim - BasicML Simulator")
        root.geometry("700x600")
        root.configure(bg=self.primary_color)

        self.create_widgets(root)

    def create_widgets(self, root):
        """Creates all GUI widgets."""
        # Menu Bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load from File", command=self.load_from_file)
        file_menu.add_command(label="Save to File", command=self.save_to_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Instruction Input
        self.instruction_label = tk.Label(root, text="Enter a BasicML Command:", bg=self.primary_color, fg="white")
        self.instruction_label.pack()

        self.command_input = tk.Entry(root, width=50, bg=self.off_color, fg="black")
        self.command_input.pack(pady=5)

        self.add_command_button = tk.Button(root, text="Add to Memory", command=self.add_command, bg=self.off_color)
        self.add_command_button.pack()

        # File Format Indicator
        self.format_label = tk.Label(root, text="File Format: None", bg=self.primary_color, fg="white")
        self.format_label.pack()

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

        self.delete_button = tk.Button(self.button_frame, text="Delete Command", command=self.delete_command, bg=self.off_color)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.modify_button = tk.Button(self.button_frame, text="Modify Command", command=self.modify_command, bg=self.off_color)
        self.modify_button.pack(side=tk.LEFT, padx=5)

        self.cut_button = tk.Button(self.button_frame, text="Cut", command=self.cut_command, bg=self.off_color)
        self.cut_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = tk.Button(self.button_frame, text="Copy", command=self.copy_command, bg=self.off_color)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.paste_button = tk.Button(self.button_frame, text="Paste", command=self.paste_command, bg=self.off_color)
        self.paste_button.pack(side=tk.LEFT, padx=5)

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

    def validate_command(self, command):
        """Validates command format based on file_format."""
        if not self.file_format:
            return True  # Allow any format if no file is loaded yet
        try:
            instruction = int(command)
            if self.file_format == 'old':
                if not (len(command) == 4 and -9999 <= instruction <= 9999):
                    messagebox.showerror("Error", "Command must be a 4-digit number (-9999 to 9999).")
                    return False
            else:  # 'new'
                if not (len(command) == 6 and -99999 <= instruction <= 99999):
                    messagebox.showerror("Error", "Command must be a 6-digit number (-99999 to 99999).")
                    return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid command. Must be an integer.")
            return False

    def check_memory_limit(self):
        """Checks if memory limit of 250 is reached."""
        if len(self.memory) >= 250:
            messagebox.showerror("Error", "Memory limit of 250 instructions reached.")
            return False
        return True

    def add_command(self):
        """Adds an individual command to memory."""
        command = self.command_input.get().strip()
        if command and self.validate_command(command) and self.check_memory_limit():
            try:
                instruction = int(command)
                index = len(self.memory)
                self.memory.append(instruction)
                self.memory_listbox.insert(tk.END, f"{index}: {instruction}")
                self.command_input.delete(0, tk.END)
                self.simulator.memory[index] = instruction  # Sync with backend
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
        """Runs the loaded program using UVSim backend."""
        if not self.memory:
            messagebox.showerror("Error", "No program loaded. Please add commands to memory first.")
            return

        self.simulator.memory[:len(self.memory)] = self.memory  # Sync memory
        self.simulator.file_format = self.file_format
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "Executing program...\n")
        try:
            self.simulator.execute()
            self.accumulator = self.simulator.accumulator
            self.instruction_counter = self.simulator.program_counter
            self.output_text.insert(tk.END, f"Execution complete.\nAccumulator: {self.accumulator}\n")
            self.accumulator_label.config(text=f"Accumulator: {self.accumulator}")
            self.instruction_counter_label.config(text=f"Instruction Counter: {self.instruction_counter}")
        except Exception as e:
            self.output_text.insert(tk.END, f"Execution error: {str(e)}\n")
        self.output_text.config(state=tk.DISABLED)

    def load_from_file(self):
        """Loads a program from a file using UVSim backend."""
        file_path = filedialog.askopenfilename(
            initialdir=self.last_directory,
            title="Select Program File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.last_directory = file_path.rsplit('/', 1)[0]
            if self.simulator.load_program_from_file(file_path):
                self.file_format = self.simulator.file_format
                self.memory = self.simulator.memory[:]
                self.memory_listbox.delete(0, tk.END)
                for i, instruction in enumerate(self.memory):
                    if instruction != 0:  # Only display non-zero memory
                        self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
                self.format_label.config(text=f"File Format: {self.file_format or 'None'}")
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"Loaded program from {file_path} ({self.file_format} format)\n")
                self.output_text.config(state=tk.DISABLED)

    def save_to_file(self):
        """Saves the current memory contents to a file in the correct format."""
        if not self.memory:
            messagebox.showerror("Error", "No program in memory to save.")
            return

        file_path = filedialog.asksaveasfilename(
            initialdir=self.last_directory,
            title="Save Program As",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.last_directory = file_path.rsplit('/', 1)[0]
            try:
                with open(file_path, 'w') as file:
                    for instruction in self.memory:
                        if self.file_format == 'old':
                            file.write(f"{instruction:04d}\n")
                        else:  # 'new' or no format
                            file.write(f"{instruction:06d}\n")
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"Program saved to {file_path}\n")
                self.output_text.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def show_help(self):
        """Displays help information."""
        messagebox.showinfo("Help", "BasicML Commands:\n"
                                   "10xxx - Read Input\n"
                                   "11xxx - Write Output\n"
                                   "20xxx - Load into Accumulator\n"
                                   "21xxx - Store from Accumulator\n"
                                   "30xxx - Add\n"
                                   "31xxx - Subtract\n"
                                   "32xxx - Divide\n"
                                   "33xxx - Multiply\n"
                                   "40xxx - Branch\n"
                                   "41xxx - Branch if Negative\n"
                                   "42xxx - Branch if Zero\n"
                                   "43xxx - Halt\n"
                                   "xxx is memory address (000-249)")

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
        self.format_label.config(bg=self.primary_color)
        self.status_frame.config(bg=self.primary_color)
        self.memory_listbox.config(bg=self.off_color, fg="black")
        self.output_text.config(bg=self.off_color, fg="black")
        self.command_input.config(bg=self.off_color, fg="black")

        buttons = [self.load_button, self.execute_button, self.file_button, self.color_button, 
                  self.help_button, self.add_command_button, self.delete_button, 
                  self.modify_button, self.cut_button, self.copy_button, self.paste_button]
        for button in buttons:
            button.config(bg=self.off_color, fg="black")

        self.button_frame.config(bg=self.primary_color)

    def delete_command(self):
        """Deletes a selected command from memory."""
        try:
            index = self.memory_listbox.curselection()[0]
            self.memory_listbox.delete(index)
            self.memory.pop(index)
            self.simulator.memory[index] = 0
            
            # Update listbox indices
            self.memory_listbox.delete(0, tk.END)
            for i, instruction in enumerate(self.memory):
                if instruction != 0:
                    self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
        except IndexError:
            messagebox.showerror("Error", "Select a command to delete.")

    def modify_command(self):
        """Modifies a selected command in memory."""
        try:
            index = self.memory_listbox.curselection()[0]
            command = self.command_input.get().strip()
            if command and self.validate_command(command):
                try:
                    instruction = int(command)
                    self.memory[index] = instruction
                    self.simulator.memory[index] = instruction
                    self.memory_listbox.delete(index)
                    self.memory_listbox.insert(index, f"{index}: {instruction}")
                    self.command_input.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("Error", "Invalid command. Must be an integer.")
            else:
                messagebox.showerror("Error", "Enter a new command to modify.")
        except IndexError:
            messagebox.showerror("Error", "Select a command to modify.")

    def copy_command(self):
        """Copies a selected command."""
        try:
            index = self.memory_listbox.curselection()[0]
            self.clipboard = str(self.memory[index])
        except IndexError:
            messagebox.showerror("Error", "Select a command to copy.")

    def cut_command(self):
        """Cuts a selected command."""
        try:
            index = self.memory_listbox.curselection()[0]
            self.clipboard = str(self.memory[index])
            self.memory_listbox.delete(index)
            self.memory.pop(index)
            self.simulator.memory[index] = 0
            
            # Update listbox indices
            self.memory_listbox.delete(0, tk.END)
            for i, instruction in enumerate(self.memory):
                if instruction != 0:
                    self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
        except IndexError:
            messagebox.showerror("Error", "Select a command to cut.")

    def paste_command(self):
        """Pastes the copied command into memory."""
        if self.clipboard and self.check_memory_limit():
            if self.validate_command(self.clipboard):
                try:
                    instruction = int(self.clipboard)
                    index = len(self.memory)
                    self.memory.append(instruction)
                    self.simulator.memory[index] = instruction
                    self.memory_listbox.insert(tk.END, f"{index}: {instruction}")
                except ValueError:
                    messagebox.showerror("Error", "Invalid command. Must be an integer.")
            else:
                messagebox.showerror("Error", "Pasted command does not match file format.")
        else:
            messagebox.showerror("Error", "Nothing to paste or memory limit reached.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSim(root)
    root.mainloop()
