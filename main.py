from tkinter import *
from tkinter import filedialog
import itertools
import time
import random
import math

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


def calculate_permutation_result(permutation):
    global cities_matrix
    global number_of_cities
    result = 0
    i = 0
    while i < len(permutation):
        if (i + 1) == number_of_cities:
            i = -1
            result = result + cities_matrix[int(permutation[i])][int(permutation[i + 1])]
            i = number_of_cities
        else:
            result = result + cities_matrix[int(permutation[i])][int(permutation[i + 1])]
            i = i + 1
    return result


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
            if (j + 1) == number_of_cities:
                j = -1
                distance = distance + cities_matrix[every_permutation[i][j]][every_permutation[i][j + 1]]
                j = number_of_cities - 1
            else:
                distance = distance + cities_matrix[every_permutation[i][j]][every_permutation[i][j + 1]]
            j = j + 1
        if distance < result:
            result = distance
            best_permutation = every_permutation[i]
        distance = 0
        i = i + 1
    end_time = time.time()
    time_sum = end_time - start_time
    result_panel.delete(0.0, END)
    result_panel.insert(INSERT, "Best result: " + str(result))
    result_panel.insert(INSERT, "\n\nBest permutation: " + str(best_permutation))
    result_panel.insert(INSERT, "\n\nCalculation time: " + str(time_sum) + "s")


def confirm_perm(type_in_perm_window, permutation_text, result_panel):
    global number_of_cities
    permutation = []
    permutation.append(permutation_text.get().split(" "))
    type_in_perm_window.destroy()
    result = 0
    i = 0
    while i < len(permutation[0]):
        if (i + 1) == number_of_cities:
            i = -1
            result = result + cities_matrix[int(permutation[0][i])][int(permutation[0][i + 1])]
            i = number_of_cities
        else:
            result = result + cities_matrix[int(permutation[0][i])][int(permutation[0][i + 1])]
            i = i + 1
    result_panel.insert(INSERT, "Permutation: " + str(permutation[0]))
    result_panel.insert(INSERT, "\n\nResult: " + str(result))


def constant_perm_method(result_panel):
    type_in_perm_window = Tk()
    type_in_perm_window.geometry('700x120')
    description_label = Label(type_in_perm_window, text="Type new permutation below (separate with spacebars):",
                              font="none 14 bold")
    description_label.pack()
    permutation_text = Entry(type_in_perm_window, width=50, font="none 14 bold")
    permutation_text.pack(pady=10)
    result_panel.delete(0.0, END)
    confirm_button = Button(type_in_perm_window, text="Confirm",
                            command=lambda: confirm_perm(type_in_perm_window, permutation_text, result_panel))
    confirm_button.pack()


def check_if_equal(first_random_number, second_random_number):
    global number_of_cities
    if first_random_number == second_random_number:
        while first_random_number == second_random_number:
            second_random_number = random.randint(1, number_of_cities)


def switch_places(first_random_number, second_random_number, permutation):
    temp_position = permutation[second_random_number]
    permutation[second_random_number] = permutation[first_random_number]
    permutation[first_random_number] = temp_position


def sa_algorithm_method(result_panel):
    global number_of_cities
    permutation = [++i for i in range(number_of_cities)]
    initial_result = calculate_permutation_result(permutation)
    current_result = initial_result
    best_result = current_result
    initial_temperature = 1000
    current_temperature = initial_temperature
    final_temperature = 0.01
    cooling_rate = 0.995
    while current_temperature > final_temperature:
        first_random_number = random.randint(1, number_of_cities - 1)
        second_random_number = random.randint(1, number_of_cities - 1)
        check_if_equal(first_random_number, second_random_number)
        switch_places(first_random_number, second_random_number, permutation)
        new_result = calculate_permutation_result(permutation)
        if best_result > new_result:
            best_result = new_result
            best_permutation = permutation[:]
        if new_result <= current_result:
            current_result = new_result
        else:
            delta = new_result - current_result
            p = math.exp(-delta / current_temperature)
            z = random.uniform(0, 1)
            if z < p:
                current_result = new_result
            current_temperature = current_temperature * cooling_rate
    result_panel.delete(0.0, END)
    result_panel.insert(INSERT, "Best permutation: " + str(best_permutation))
    result_panel.insert(INSERT, "\n\nResult: " + str(best_result))


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
        all_perm_algorithm_button = Button(algorithm_panel, command=lambda: all_perm_method(result_panel),
                                           text="All permutations")
        const_perm_algorithm_button = Button(algorithm_panel, command=lambda: constant_perm_method(result_panel),
                                             text="Constant permutation")
        sa_algorithm_button = Button(algorithm_panel, command=lambda: sa_algorithm_method(result_panel),
                                     text="SA algorithm")
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
