from tkinter import *
from tkinter import filedialog


def run():
    root = Tk()
    ui = Window(root)
    ui.root.mainloop()


def open_matrix(matrix_panel):
    matrix_file = filedialog.askopenfilename(defaultextension=".txt")
    matrix_file = open(matrix_file, 'r')
    matrix_panel.delete(0.0, END)
    matrix_panel.insert(0.0, matrix_file.read())
    matrix_file.close()


class Window:
    def __init__(self, root):
        self.root = root
        self.configure_root()
        matrix_panel = self.create_matrix_panel()
        self.create_result_panel()
        control_panel = self.create_control_panel(matrix_panel)
        self.create_algorithm_panel()

    def configure_root(self):
        self.root.geometry("1920x1024")
        self.root.title("Solving traveling salesman problem")

    def create_control_panel(self, matrix_panel):
        control_panel = Frame(self.root, width=200, height=1024)
        control_panel.place(x=0, y=100)
        load_matrix_button = Button(control_panel, command=lambda: open_matrix(matrix_panel), text="Load Matrix")
        add_city_button = Button(control_panel, bg="grey", text="Add city")
        delete_last_city_button = Button(control_panel, bg="grey", text="Delete last city")
        erase_all_button = Button(control_panel, bg="grey", text="Erase all cities")
        create_matrix_button = Button(control_panel, bg="grey", text="Create new Matrix")
        save_results_button = Button(control_panel, bg="grey", text="Save results")
        quit_button = Button(control_panel, command=quit, text="Quit")
        load_matrix_button.pack(padx=50)
        add_city_button.pack(pady=50)
        delete_last_city_button.pack()
        erase_all_button.pack(pady=50)
        create_matrix_button.pack()
        save_results_button.pack(pady=50)
        quit_button.pack()
        return control_panel

    def create_algorithm_panel(self):
        algorithm_panel = Frame(self.root, width=200, height=1024)
        algorithm_panel.place(x=200, y=100)
        all_perm_algorithm_button = Button(algorithm_panel, bg="grey", text="All permutations")
        const_perm_algorithm_button = Button(algorithm_panel, bg="grey", text="Constant permutation")
        sa_algorithm_button = Button(algorithm_panel, bg="grey", text="SA algorithm")
        all_perm_algorithm_button.pack(padx=50)
        const_perm_algorithm_button.pack(pady=50)
        sa_algorithm_button.pack()

    def create_matrix_panel(self):
        matrix_panel = Text(self.root, width=172, height=40, bg="lightgrey")
        matrix_panel.place(x=450, y=20)
        return matrix_panel

    def create_result_panel(self):
        result_panel = Frame(self.root, width=1380, height=250, bg="grey")
        result_panel.place(x=450, y=740)


run()
