import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
from UVSim import UVSim as UVSimBackend

class UVSimTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.background_frame = tk.Frame(self, bg="#4C721D")
        self.background_frame.pack(fill=tk.BOTH, expand=True)
        
        self.simulator = UVSimBackend()
        self.memory = []
        self.accumulator = 0
        self.instruction_counter = 0
        self.last_directory = ""
        self.file_format = None
        self.clipboard = None
        self.primary_color = "#4C721D"
        self.off_color = "#FFFFFF"
        
        self.create_widgets()

    def create_widgets(self):
        
        # Instruction Input
        self.instruction_label = tk.Label(self.background_frame, text="Enter a BasicML Command:", 
                                         bg=self.primary_color, fg="white")
        self.instruction_label.pack()

        self.command_input = tk.Entry(self.background_frame, width=50, bg=self.off_color, fg="black")
        self.command_input.pack(pady=5)

        self.add_command_button = tk.Button(self.background_frame, text="Add to Memory", 
                                           command=self.add_command, bg=self.off_color)
        self.add_command_button.pack()

        # File Format Indicator
        self.format_label = tk.Label(self.background_frame, text="File Format: None", 
                                    bg=self.primary_color, fg="white")
        self.format_label.pack()

        # Memory Display
        self.memory_label = tk.Label(self.background_frame, text="Memory:", 
                                    bg=self.primary_color, fg="white")
        self.memory_label.pack()

        self.memory_listbox = tk.Listbox(self.background_frame, height=10, bg=self.off_color, fg="black")
        self.memory_listbox.pack(fill=tk.X, padx=10, pady=5)

        # Control Buttons
        self.button_frame = tk.Frame(self.background_frame, bg=self.primary_color)
        self.button_frame.pack(pady=5)

        buttons = [
            ("Load Program", self.load_program),
            ("Execute", self.execute_program),
            ("Load from File", self.load_from_file),
            ("Delete Command", self.delete_command),
            ("Modify Command", self.modify_command),
            ("Cut", self.cut_command),
            ("Copy", self.copy_command),
            ("Paste", self.paste_command),
            ("Help", self.show_help),
        ]
        
        for text, command in buttons:
            button = tk.Button(self.button_frame, text=text, command=command, bg=self.off_color)
            button.pack(side=tk.LEFT, padx=5)

        # Status Display
        self.status_frame = tk.Frame(self.background_frame, bg=self.primary_color)
        self.status_frame.pack(pady=5)

        self.accumulator_label = tk.Label(self.status_frame, text=f"Accumulator: {self.accumulator}", 
                                        bg=self.primary_color, fg="white")
        self.accumulator_label.pack(side=tk.LEFT, padx=10)

        self.instruction_counter_label = tk.Label(self.status_frame,
                                                text=f"Instruction Counter: {self.instruction_counter}", 
                                                bg=self.primary_color, fg="white")
        self.instruction_counter_label.pack(side=tk.LEFT, padx=10)

        # Output Display
        self.output_label = tk.Label(self.background_frame, text="Output:", bg=self.primary_color, fg="white")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(self.background_frame, height=10, state=tk.DISABLED,
                                                     bg=self.off_color, fg="black")
        self.output_text.pack(fill=tk.X, padx=10, pady=5)
        
        bottom_buttons_frame = tk.Frame(self.background_frame, bg=self.primary_color)
        bottom_buttons_frame.pack(pady=10)

        self.change_colors_button = tk.Button(bottom_buttons_frame, text="Change Colors", 
                                             command=self.change_colors, bg=self.off_color)
        self.change_colors_button.pack(side=tk.LEFT)

    def validate_command(self, command):
        """Validates command format based on file_format."""
        if not self.file_format:
            return True
        try:
            instruction = int(command)
            if self.file_format == 'old':
                if not (len(command) == 4 and -9999 <= instruction <= 9999):
                    messagebox.showerror("Error", "Command must be a 4-digit number (-9999 to 9999).")
                    return False
            else:
                if not (len(command) == 6 and -99999 <= instruction <= 99999):
                    messagebox.showerror("Error", "Command must be a 6-digit number (-99999 to 99999).")
                    return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid command. Must be an integer.")
            return False

    def check_memory_limit(self):
        if len(self.memory) >= 250:
            messagebox.showerror("Error", "Memory limit of 250 instructions reached.")
            return False
        return True

    def add_command(self):
        command = self.command_input.get().strip()
        if command and self.validate_command(command) and self.check_memory_limit():
            try:
                instruction = int(command)
                index = len(self.memory)
                self.memory.append(instruction)
                self.memory_listbox.insert(tk.END, f"{index}: {instruction}")
                self.command_input.delete(0, tk.END)
                self.simulator.memory[index] = instruction
            except ValueError:
                messagebox.showerror("Error", "Invalid command. Must be an integer.")

    def load_program(self):
        if not self.memory:
            messagebox.showerror("Error", "No commands in memory to load.")
            return
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "Program loaded into memory.\n")
        self.output_text.config(state=tk.DISABLED)

    def execute_program(self):
        if not self.memory:
            messagebox.showerror("Error", "No program loaded. Add commands first.")
            return
        self.simulator.memory[:len(self.memory)] = self.memory
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
                    if instruction != 0:
                        self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
                self.format_label.config(text=f"File Format: {self.file_format or 'None'}")
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"Loaded program from {file_path} ({self.file_format} format)\n")
                self.output_text.config(state=tk.DISABLED)

    def save_to_file(self):
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
                        else:
                            file.write(f"{instruction:06d}\n")
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"Program saved to {file_path}\n")
                self.output_text.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def show_help(self):
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
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        if primary_color:
            self.primary_color = primary_color

        off_color = colorchooser.askcolor(title="Choose Off Color")[1]
        if off_color:
            self.off_color = off_color

        self.apply_colors()

    def apply_colors(self):
        # Update background frame color
        self.background_frame.config(bg=self.primary_color)
        
        # Update labels and frames with primary color
        for widget in [self.instruction_label,
                    self.format_label,
                    self.memory_label,
                    self.output_label,
                    *self.status_frame.winfo_children()]:
            widget.config(bg=self.primary_color)
        
        for frame in [self.button_frame,
                    self.status_frame]:
            frame.config(bg=self.primary_color)
        
        for button in [self.add_command_button, 
                    self.change_colors_button,
                    *[child for child in self.button_frame.winfo_children() if isinstance(child, tk.Button)]]:
            button.config(bg=self.off_color)
        
        for widget in [self.command_input,
                    self.memory_listbox,
                    self.output_text]:
            widget.config(bg=self.off_color)

    def delete_command(self):
        try:
            index = self.memory_listbox.curselection()[0]
            self.memory_listbox.delete(index)
            self.memory.pop(index)
            self.simulator.memory[index] = 0
            self.memory_listbox.delete(0, tk.END)
            for i, instruction in enumerate(self.memory):
                if instruction != 0:
                    self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
        except IndexError:
            messagebox.showerror("Error", "Select a command to delete.")

    def modify_command(self):
        try:
            index = self.memory_listbox.curselection()[0]
            command = self.command_input.get().strip()
            if command and self.validate_command(command):
                instruction = int(command)
                self.memory[index] = instruction
                self.simulator.memory[index] = instruction
                self.memory_listbox.delete(index)
                self.memory_listbox.insert(index, f"{index}: {instruction}")
                self.command_input.delete(0, tk.END)
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Invalid selection or command")

    def copy_command(self):
        try:
            index = self.memory_listbox.curselection()[0]
            self.clipboard = str(self.memory[index])
        except IndexError:
            messagebox.showerror("Error", "Select a command to copy")

    def cut_command(self):
        try:
            index = self.memory_listbox.curselection()[0]
            self.clipboard = str(self.memory[index])
            self.memory_listbox.delete(index)
            self.memory.pop(index)
            self.simulator.memory[index] = 0
            self.memory_listbox.delete(0, tk.END)
            for i, instruction in enumerate(self.memory):
                if instruction != 0:
                    self.memory_listbox.insert(tk.END, f"{i}: {instruction}")
        except IndexError:
            messagebox.showerror("Error", "Select a command to cut")

    def paste_command(self):
        if self.clipboard and self.check_memory_limit():
            if self.validate_command(self.clipboard):
                try:
                    instruction = int(self.clipboard)
                    index = len(self.memory)
                    self.memory.append(instruction)
                    self.simulator.memory[index] = instruction
                    self.memory_listbox.insert(tk.END, f"{index}: {instruction}")
                except ValueError:
                    messagebox.showerror("Error", "Invalid command")
            else:
                messagebox.showerror("Error", "Invalid format for pasted command")
        else:
            messagebox.showerror("Error", "Nothing to paste or memory full")

class UVSimApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UVSim - BasicML Simulator")
        self.geometry("700x630")
        
        # Create Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        # Add first tab
        self.add_tab()
        
        # Menu for tabs
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Tab", command=self.add_tab)
        file_menu.add_command(label="Close Tab", command=self.close_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

    def add_tab(self):
        new_tab = UVSimTab(self.notebook)
        self.notebook.add(new_tab, text=f"Tab {self.notebook.index('end')+1}")

    def close_tab(self):
        if self.notebook.index("end") > 1:
            self.notebook.forget(self.notebook.select())

if __name__ == "__main__":
    app = UVSimApp()
    app.mainloop()
