from tkinter import *
from tkinter import filedialog
import itertools
import time

number_of_cities = 0
cities_matrix = []


def run():
    root = Tk()
    ui = Window(root)
    ui.root.mainloop()


def open_matrix(matrix_panel, info_panel):
    global number_of_cities
    global cities_matrix
    cities_matrix = []
    number_of_cities = 0
    matrix_file = filedialog.askopenfilename(defaultextension=".txt")
    matrix_file = open(matrix_file, 'r')
    matrix_panel.delete(0.0, END)
    matrix_panel.insert(0.0, matrix_file.read())
    matrix_file.seek(0, 0)
    for index in matrix_file.readlines():
        number_of_cities = number_of_cities + 1
    matrix_file.seek(0, 0)
    for index in range(number_of_cities):
        content = matrix_file.readline().split(" ")
        content = [int(i) for i in content]
        cities_matrix.append(content)
    matrix_file.seek(0, 0)
    matrix_file.close()
    info_panel.config(text="Current number of cities: " + str(number_of_cities))


def all_perm_method(result_panel):
    global number_of_cities
    initial_permutation = [++i for i in range(number_of_cities)]
    every_permutation = list(itertools.permutations(initial_permutation))
    distance = 0
    i = 0
    result = 500000
    start_time = time.time()
    while i < len(every_permutation):
        j = 0
        while j < number_of_cities:
            if (j+1) == number_of_cities:
                j = -1
                distance = distance + cities_matrix[every_permutation[i][j]][every_permutation[i][j+1]]
                j = number_of_cities-1
            else:
                distance = distance + cities_matrix[every_permutation[i][j]][every_permutation[i][j + 1]]
            j = j+1
        if distance < result:
            result = distance
            best_permutation = every_permutation[i]
        distance = 0
        i = i+1
    end_time = time.time()
    time_sum = end_time - start_time
    result_panel.delete(0.0, END)
    result_panel.insert(INSERT, "Best result: " + str(result))
    result_panel.insert(INSERT, "\n\nBest permutation: " + str(best_permutation))
    result_panel.insert(INSERT, "\n\nCalculation time: " + str(time_sum) + "s")


class Window:
    def __init__(self, root):
        self.root = root
        self.configure_root()
        info_panel = self.create_info_panel()
        matrix_panel = self.create_matrix_panel()
        result_panel = self.create_result_panel()
        control_panel = self.create_control_panel(matrix_panel, info_panel)
        self.create_algorithm_panel(result_panel)

    def configure_root(self):
        self.root.geometry("1920x1024")
        self.root.title("Solving traveling salesman problem")

    def create_control_panel(self, matrix_panel, info_panel):
        control_panel = Frame(self.root, width=200, height=1024)
        control_panel.place(x=0, y=100)
        load_matrix_button = Button(control_panel, command=lambda: open_matrix(matrix_panel, info_panel),
                                    text="Load Matrix")
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

    def create_algorithm_panel(self, result_panel):
        algorithm_panel = Frame(self.root, width=200, height=1024)
        algorithm_panel.place(x=200, y=100)
        all_perm_algorithm_button = Button(algorithm_panel, command=lambda: all_perm_method(result_panel), text="All permutations")
        const_perm_algorithm_button = Button(algorithm_panel, bg="grey", text="Constant permutation")
        sa_algorithm_button = Button(algorithm_panel, bg="grey", text="SA algorithm")
        all_perm_algorithm_button.pack(padx=50)
        const_perm_algorithm_button.pack(pady=50)
        sa_algorithm_button.pack()

    def create_matrix_panel(self):
        matrix_panel = Text(self.root, width=172, height=38, bg="lightgrey")
        matrix_panel.place(x=450, y=60)
        return matrix_panel

    def create_result_panel(self):
        result_panel = Text(self.root, width=172, height=15, bg="grey")
        result_panel.place(x=450, y=740)
        return result_panel

    def create_info_panel(self):
        info_panel = Label(self.root, text="Current number of cities: " + str(number_of_cities))
        info_panel.place(x=450, y=20)
        info_panel.config(font=("Courier", 20))
        return info_panel


run()
