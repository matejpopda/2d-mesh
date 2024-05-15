import tkinter as tk
from draw import MainWindow
import random

def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    random.seed(123456879)
    main()
