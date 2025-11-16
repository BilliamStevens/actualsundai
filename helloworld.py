import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

class GraphingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Graphing Calculator")
        self.root.geometry("800x600")
        
        # Set up the main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Function Input", padding=10)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Function input
        ttk.Label(self.input_frame, text="y = ").pack(side=tk.LEFT)
        self.function_entry = ttk.Entry(self.input_frame, width=40)
        self.function_entry.pack(side=tk.LEFT, padx=5)
        self.function_entry.insert(0, "x**2")  # Default function
        
        # Plot button
        self.plot_button = ttk.Button(self.input_frame, text="Plot", command=self.plot_function)
        self.plot_button.pack(side=tk.LEFT, padx=5)
        
        # Range frame
        self.range_frame = ttk.Frame(self.main_frame)
        self.range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # X range
        ttk.Label(self.range_frame, text="X min:").pack(side=tk.LEFT)
        self.xmin_entry = ttk.Entry(self.range_frame, width=8)
        self.xmin_entry.pack(side=tk.LEFT, padx=5)
        self.xmin_entry.insert(0, "-10")
        
        ttk.Label(self.range_frame, text="X max:").pack(side=tk.LEFT)
        self.xmax_entry = ttk.Entry(self.range_frame, width=8)
        self.xmax_entry.pack(side=tk.LEFT, padx=5)
        self.xmax_entry.insert(0, "10")
        
        # Create plot area
        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add some styling
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        
        # Add some example buttons for common functions
        self.add_example_buttons()
        
        # Plot the default function
        self.plot_function()
    
    def add_example_buttons(self):
        example_frame = ttk.Frame(self.main_frame)
        example_frame.pack(fill=tk.X, pady=(10, 0))
        
        examples = [
            ("x^2", "x**2"),
            ("sin(x)", "np.sin(x)"),
            ("cos(x)", "np.cos(x)"),
            ("e^x", "np.exp(x)"),
            ("ln(x)", "np.log(x)"),
            ("1/x", "1/x")
        ]
        
        for text, func in examples:
            btn = ttk.Button(
                example_frame, 
                text=text,
                command=lambda f=func: self.set_function(f)
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def set_function(self, func):
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, func)
        self.plot_function()
    
    def safe_eval(self, expr, x):
        # Replace ^ with ** for exponentiation
        expr = expr.replace('^', '**')
        
        # Replace common math functions with numpy equivalents
        expr = re.sub(r'\b(sin|cos|tan|exp|log|sqrt)\b', r'np.\1', expr)
        
        # Define allowed names for eval
        allowed_names = {
            'x': x,
            'np': np,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'log': np.log,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'e': np.e
        }
        
        # Compile the expression for better performance
        code = compile(expr, '<string>', 'eval')
        
        # Check for disallowed names
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Use of {name} not allowed")
        
        # Evaluate the expression
        return eval(code, {'__builtins__': {}}, allowed_names)
    
    def plot_function(self):
        try:
            # Get function and range
            func_str = self.function_entry.get().strip()
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
            
            # Generate x values
            x = np.linspace(x_min, x_max, 400)
            
            # Evaluate the function
            y = self.safe_eval(func_str, x)
            
            # Clear previous plot
            self.ax.clear()
            
            # Plot the function
            self.ax.plot(x, y, 'b-', linewidth=2)
            
            # Add grid and labels
            self.ax.grid(True, alpha=0.3)
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title(f'Graph of y = {func_str}')
            
            # Adjust layout and redraw
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid function or range: {str(e)}")

def main():
    root = tk.Tk()
    app = GraphingCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()