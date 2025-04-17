import customtkinter as ctk
from CTkXYFrame import *
import numpy as np

from main import matrix_inv, matrix_rang, multiply_matrix, multiply_num, exponentiation_matrix, compose_matrix, \
    check_same_size, subtract_matrix, check_multiply_sizes, check_square, determinant


class Matrix(ctk.CTkFrame):
    def __init__(self, master, name):
        super().__init__(master)
        # Тайтл
        self.columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.title_A = ctk.CTkLabel(self, text=f'Матрица {name}', font=('Arial', 15))
        self.title_A.grid(row=0, column=0, columnspan=2)

        # Размер, очистить
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, padx=5)

        self.rows = ctk.CTkComboBox(self.buttons_frame, values=[str(i) for i in range(1, 11)], width=55,
                                    state='readonly', command=self.build)
        self.rows.set('5')
        self.rows.grid(row=0, column=0, padx=(5, 0), pady=5)

        self.x = ctk.CTkLabel(self.buttons_frame, text='X')
        self.x.grid(row=0, column=1, padx=5, pady=5)

        self.columns = ctk.CTkComboBox(self.buttons_frame, values=[str(i) for i in range(1, 11)], width=55,
                                       state='readonly', command=self.build)
        self.columns.set('5')
        self.columns.grid(row=0, column=2, pady=5)

        self.clear_btn = ctk.CTkButton(self.buttons_frame, text='Очистить', width=10, command=self.clear)
        self.clear_btn.grid(row=0, column=3, padx=5, pady=5)

        # Матрица
        self.matrix_frame = ctk.CTkFrame(self)
        self.matrix_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.entries_list = []
        self.build(None)

    def build(self, k, arr=None):
        self.entries_list.clear()
        for ent in self.matrix_frame.winfo_children():
            ent.destroy()
        if arr is None:
            m = int(self.rows.get())
            n = int(self.columns.get())
            for i in range(m):
                for j in range(n):
                    entry = ctk.CTkEntry(self.matrix_frame, width=55)
                    self.entries_list.append(entry)
                    entry.grid(row=i, column=j)
        else:
            m = len(arr)
            n = len(arr[0])
            self.rows.set(str(m))
            self.columns.set(str(n))
            for i in range(m):
                for j in range(n):
                    entry = ctk.CTkEntry(self.matrix_frame, width=55)
                    entry.insert(0, str(arr[i][j]))
                    self.entries_list.append(entry)
                    entry.grid(row=i, column=j)

    def clear(self):
        for ent in self.entries_list:
            ent.delete(0, len(ent.get()))

    def get_matrix(self):
        try:
            m = int(self.rows.get())
            n = int(self.columns.get())
            res = []
            for i in range(0, m * n, n):
                res.append([float(ent.get()) for ent in self.entries_list[i:i + n]])
            return res
        except:
            return 'Проверьте введенные данные'


class Result(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Тайтл
        self.title_A = ctk.CTkLabel(self, text='Результат', font=('Arial', 15))
        self.title_A.grid(row=0, column=0, columnspan=2)
        self.columnconfigure((0, 1), weight=1)

        # Результат
        self.rowconfigure(1, weight=1)
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.columnconfigure((0, 1), weight=1)
        self.result_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.current_res = None
        self.current_matrix = None

        # Кнопки для копирования
        self.copy_to_A_btn = ctk.CTkButton(self, text='Копировать в А', command=self.copy_to_A_btn_event)
        self.copy_to_A_btn.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.copy_to_B_btn = ctk.CTkButton(self, text='Копировать в B', command=self.copy_to_B_btn_event)
        self.copy_to_B_btn.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def res_text(self, output):
        for el in self.result_frame.winfo_children():
            el.destroy()
        res = ctk.CTkLabel(self.result_frame, text=output, padx=3)
        res.grid(row=0, column=0, columnspan=2)
        self.current_res = 'text'

    def res_matrix(self, array):
        for el in self.result_frame.winfo_children():
            el.destroy()

        matrix = ctk.CTkFrame(self.result_frame)
        matrix.grid(row=0, column=0, columnspan=2)
        for i in range(len(array)):
            for j in range(len(array[0])):
                entry = ctk.CTkEntry(matrix, width=55)
                entry.insert(0, string=str(array[i][j]))
                entry.configure(state='disabled')
                entry.grid(row=i, column=j)
        self.current_res = 'matrix'
        self.current_matrix = array

    def copy_to_A_btn_event(self):
        if self.current_res in (None, 'text'):
            pass
        else:
            app.matrix_frame.matrix_A.build(None, arr=self.current_matrix)

    def copy_to_B_btn_event(self):
        if self.current_res in (None, 'text'):
            pass
        else:
            app.matrix_frame.matrix_B.build(None, arr=self.current_matrix)


class Operations(ctk.CTkFrame):
    def __init__(self, master, linked_matrix):
        super().__init__(master)
        self.linked_matrix = linked_matrix
        self.columnconfigure(0, weight=1)

        self.transpose_btn = ctk.CTkButton(self, text='Транспонировать', command=self.transpose_btn_event)
        self.transpose_btn.grid(row=0, column=0, pady=5, columnspan=2)

        self.determinant_btn = ctk.CTkButton(self, text='Найти определитель', command=self.determinant_btn_event)
        self.determinant_btn.grid(row=1, column=0, pady=5, columnspan=2)

        self.inverse_btn = ctk.CTkButton(self, text='Найти обратную', command=self.inverse_btn_event)
        self.inverse_btn.grid(row=2, column=0, pady=5, columnspan=2)

        self.rang_btn = ctk.CTkButton(self, text='Найти ранг', command=self.rang_btn_event)
        self.rang_btn.grid(row=3, column=0, pady=5, columnspan=2)

        self.multiply_by_number_btn = ctk.CTkButton(self, text='Умножить на число',
                                                    command=self.multiply_by_number_btn_event)
        self.multiply_by_number_btn.grid(row=4, column=0, pady=5, columnspan=2)
        self.number = ctk.CTkEntry(self, width=50)
        self.number.grid(row=4, column=1, padx=(0, 15))

        self.power_btn = ctk.CTkButton(self, text='Возвести в степень', command=self.power_btn_event)
        self.power_btn.grid(row=5, column=0, pady=5, columnspan=2)
        self.power = ctk.CTkEntry(self, width=50)
        self.power.grid(row=5, column=1, padx=(0, 15))

    def transpose_btn_event(self):
        arr = self.linked_matrix.get_matrix()
        if isinstance(arr, list):
            m = len(arr)
            n = len(arr[0])
            new = [[0] * m for _ in range(n)]
            for i in range(n):
                for j in range(m):
                    new[i][j] = arr[j][i]
            app.matrix_frame.result.res_matrix(new)
        else:
            app.matrix_frame.result.res_text(arr)

    def determinant_btn_event(self):
        arr = self.linked_matrix.get_matrix()
        if  not (isinstance(arr, list)):
            app.matrix_frame.result.res_text('Проверьте введенные данные')
        elif not(check_square(arr)):
            app.matrix_frame.result.res_text('Матрица не квадратная')
        else:
            det = determinant(arr)
            app.matrix_frame.result.res_text(det)
        '''
        ЗДЕСЬ НАЙТИ ОПРЕДЕЛИТЕЛЬ ДЛЯ arr
        (учесть что arr может быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''

    def inverse_btn_event(self):
        arr = self.linked_matrix.get_matrix()
        if not (isinstance(arr, list)):
            app.matrix_frame.result.res_text('Проверьте введенные данные')
        elif not(check_square(arr)):
            app.matrix_frame.result.res_text('Матрица не квадратная')
        elif determinant(arr)==0:
            app.matrix_frame.result.res_text('Определитель матрицы равен 0')
        else:
            matrix=matrix_inv(arr)
            app.matrix_frame.result.res_matrix(matrix)
        '''
        ЗДЕСЬ НАЙТИ ОБРАТНУЮ ДЛЯ arr
        (учесть что arr может быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_matrix() - для вывода матрицы (передать двумерный list)
        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''

    def rang_btn_event(self):
        arr = self.linked_matrix.get_matrix()
        if isinstance(arr, list):
            rang=matrix_rang(arr)
            app.matrix_frame.result.res_text(rang)
        else:
            app.matrix_frame.result.res_text(arr)
        '''
        ЗДЕСЬ НАЙТИ РАНГ arr
        (учесть что arr может быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''

    def multiply_by_number_btn_event(self):
        try:
            num = float(self.number.get())
        except ValueError:
            app.matrix_frame.result.res_text('Некорректное число для умножения')
            return None
        arr = self.linked_matrix.get_matrix()
        if isinstance(arr, list):
            matrix=multiply_num(num,arr)
            app.matrix_frame.result.res_matrix(matrix)
        else:
            app.matrix_frame.result.res_text(arr)
        '''
        ЗДЕСЬ УМНОЖИТЬ arr НА num
        (учесть что arr может быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_matrix() - для вывода матрицы (передать двумерный list)
        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''

    def power_btn_event(self):
        try:
            power = int(self.power.get())
        except ValueError:
            app.matrix_frame.result.res_text('Некорректный показатель степени')
            return None
        arr = self.linked_matrix.get_matrix()
        if isinstance(arr, list):
            matrix=exponentiation_matrix(power,arr)
            app.matrix_frame.result.res_matrix(matrix)
        else:
            app.matrix_frame.result.res_text(arr)
        '''
        ЗДЕСЬ ВОЗВЕСТИ arr В СТЕПЕНЬ power
        (учесть что arr может быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_matrix() - для вывода матрицы (передать двумерный list)
        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''


class MatrixFrame(CTkXYFrame):  # окно матричного калькулятора
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_columnconfigure((0, 2), weight=0)

        # Кнопки - + X
        self.operations = ctk.CTkFrame(self)
        self.operations.grid(row=0, column=1, sticky='ew')
        self.operations.grid_rowconfigure((0, 1, 2), weight=1)
        self.operations.grid_columnconfigure(0, weight=1)

        self.minus_btn = ctk.CTkButton(self.operations, text='-', width=50, height=2, command=self.minus_btn_event)
        self.plus_btn = ctk.CTkButton(self.operations, text='+', width=50, height=2, command=self.plus_btn_event)
        self.multiply_btn = ctk.CTkButton(self.operations, text='X', width=50, height=3,
                                          command=self.multiply_btn_event)
        self.minus_btn.grid(row=0, column=0, padx=5, pady=(5, 0), sticky='news')
        self.plus_btn.grid(row=1, column=0, padx=5, pady=(5, 5), sticky='news')
        self.multiply_btn.grid(row=2, column=0, padx=5, pady=(0, 5), sticky='news')
        # Матрица А
        self.matrix_A = Matrix(self, 'А')
        self.matrix_A.grid(row=0, column=0, sticky='news', padx=5, pady=5)
        # Операции над матрицей А
        self.matrixA_Buttons = Operations(self, self.matrix_A)
        self.matrixA_Buttons.grid(row=1, column=0, sticky='news', padx=5)
        # Матрица B
        self.matrix_B = Matrix(self, 'B')
        self.matrix_B.grid(row=0, column=2, sticky='news', padx=5, pady=5)
        # Операции над матрицей В
        self.matrixB_Buttons = Operations(self, linked_matrix=self.matrix_B)
        self.matrixB_Buttons.grid(row=1, column=2, sticky='news', padx=5)
        # Результат
        self.result = Result(self)
        self.result.grid(row=0, column=3, sticky='news', padx=(0, 5), pady=5)
        self.columnconfigure(3, weight=1)

    def plus_btn_event(self):
        matA = self.matrix_A.get_matrix()
        matB = self.matrix_B.get_matrix()
        if not(isinstance(matA, list)) or not(isinstance(matB, list)):
            app.matrix_frame.result.res_text('Проверьте введенные данные')
        elif not(check_same_size(matA,matB)):
            app.matrix_frame.result.res_text('Размеры матриц не соответствуют')
        else:
            matrix = compose_matrix(matA, matB)
            app.matrix_frame.result.res_matrix(matrix)
        '''
        ЗДЕСЬ СЛОЖИТЬ matA И matB
        (учесть что matA и matB могут быть строкой 'проверьте введенные данные', см. transpose_btn_event)
        
        app.matrix_frame.result.res_matrix() - для вывода матрицы (передать двумерный list)
        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''

    def minus_btn_event(self):
        matA = self.matrix_A.get_matrix()
        matB = self.matrix_B.get_matrix()
        if not(isinstance(matA, list)) or not(isinstance(matB, list)):
            app.matrix_frame.result.res_text('Проверьте введенные данные')
        elif not(check_same_size(matA,matB)):
            app.matrix_frame.result.res_text('Размеры матриц не соответствуют')
        else:
            matrix = subtract_matrix(matA, matB)
            app.matrix_frame.result.res_matrix(matrix)
        '''
        ЗДЕСЬ ВЫЧЕСТЬ matB ИЗ matA
        (учесть что matA и matB могут быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_matrix() - для вывода матрицы (передать двумерный list)
        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''

    def multiply_btn_event(self):
        matA = self.matrix_A.get_matrix()
        matB = self.matrix_B.get_matrix()
        if not(isinstance(matA, list)) or not(isinstance(matB, list)):
            app.matrix_frame.result.res_text('Проверьте введенные данные')
        elif not(check_multiply_sizes(matA,matB)):
            app.matrix_frame.result.res_text('Размеры матриц некорректны для операции умножения')
        else:
            matrix = multiply_matrix(matA, matB)
            app.matrix_frame.result.res_matrix(matrix)
        '''
        ЗДЕСЬ УМНОЖИТЬ matA НА matB
        (учесть что matA и matB могут быть строкой 'проверьте введенные данные', см. transpose_btn_event)

        app.matrix_frame.result.res_matrix() - для вывода матрицы (передать двумерный list)
        app.matrix_frame.result.res_text() - для вывода текста (передать str)
        '''


"""Класс, который реализует работу со СЛАУ"""


class Slau(CTkXYFrame):  # решение СЛАУ
    def __init__(self, master):
        super().__init__(master)
        # создание ячейки с выбором кол-ва неизвестных элементов
        self.text_label = ctk.CTkLabel(self, text="Выберете кол-во\nнеизвестных", anchor='center', width=12,
                                       fg_color="gray")
        self.text_label.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        self.unknown_num = ctk.CTkComboBox(self.text_label, values=[str(i) for i in range(1, 11)],
                                           command=self.bild_slau_and_button,
                                           width=55, state='readonly')
        self.unknown_num.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.slau_frame = None
        # массивы, в которые хранятся элементы СЛАУ
        self.entries_A = []
        self.entries_B = []

    def bild_slau_and_button(self, n):
        """Функция создает СЛАУ размером NxN, кнопки 'Очистить' и 'Результат' и рамку с результатом"""
        self.entries_A.clear()
        self.entries_B.clear()
        # создание рамки, в которой создается СЛАУ
        if self.slau_frame:
            self.slau_frame.destroy()  # удаляет весь фрейм
        self.slau_frame = ctk.CTkFrame(self, height=300)
        self.slau_frame.grid(row=1, column=0, padx=10, pady=10, sticky='news')
        position = 0
        for i in range(int(n)):
            row = []
            for j in range(int(n)):
                entry = ctk.CTkEntry(self.slau_frame, width=50)
                entry.grid(row=i, column=position, padx=5, pady=5)
                row.append(entry)
                self.label = ctk.CTkLabel(self.slau_frame,
                                          text=f"{f'X{j + 1} +' if j < int(n) - 1 else f'X{j + 1} = '}")
                self.label.grid(row=i, column=position + 1, padx=5, pady=5, sticky="w")
                position += 2
            position = 0
            self.entries_A.append(row)

            entry_b = ctk.CTkEntry(self.slau_frame, width=50)
            entry_b.grid(row=i, column=21, padx=5, pady=5)
            self.entries_B.append(entry_b)
        # создаем кнопку "Очистить"
        self.button_clear = ctk.CTkButton(self, text="Очистить", anchor='center', command=self.clear_slau)
        self.button_clear.grid(row=2, column=0, padx=0, pady=0, sticky='news')
        # создаем кнопку "Результат"
        self.button_result = ctk.CTkButton(self, text="Результат", anchor='center', command=self.result_slau)
        self.button_result.grid(row=1, column=1, padx=10, pady=10, sticky='e')
        # фрейм с результатом
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.grid(row=1, column=2, padx=10, pady=10, sticky='news')
        self.text_result = ctk.CTkLabel(self, text='Результат', fg_color="gray")
        self.text_result.grid(row=0, column=2, padx=10, pady=10, sticky='news')

    def clear_slau(self):
        """Функция удаляет все элементы из СЛАУ"""
        for row in self.entries_A:
            for entry in row:
                print(entry.get())
                entry.delete(0, ctk.END)
        for entry in self.entries_B:
            print(entry.get())
            entry.delete(0, ctk.END)

    def result_slau(self):
        """Функция, которая обрабатывает СЛАУ и выводит результат"""
        """Здесь происходит основные задача. entries_A - двухмерный массив,каждая строка содержит все значения при неизвестных.
          entries_В - одномерный массив хранят столбец свободных членов . Для того чтобы получить из из массивов нужно воспользоваться 
         методом get()
        """


class Navbar(ctk.CTkFrame):  # навигационная панель
    def __init__(self, master):
        super().__init__(master)
        self.matrix_btn = ctk.CTkButton(self, text="Матричный\nкалькулятор", command=self.matrix_button_event,
                                        font=('Arial', 30), border_color='black', corner_radius=0, border_width=3)
        self.matrix_btn.grid(row=0, column=0, sticky='ew')

        self.slau_btn = ctk.CTkButton(self, text="Решение СЛАУ", command=self.slau_button_event, font=('Arial', 30),
                                      border_color='black', corner_radius=0, border_width=3)
        self.slau_btn.grid(row=1, column=0, pady=5, sticky='ew')

    def matrix_button_event(self):
        App.select_frame_by_name(app, "Матричный калькулятор")

    def slau_button_event(self):
        App.select_frame_by_name(app, "Решение СЛАУ")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("МЕГАТРОН")  # название приложения
        self.geometry('1270x615')  # разрешение
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.left_panel = Navbar(self)  # навигационная панель
        self.left_panel.grid(row=0, column=0, padx=0, pady=0, sticky='wns')
        self.matrix_frame = MatrixFrame(self)  # фрейм матричного калькулятора
        self.slau_frame = Slau(self)  # фрейм калькулятора СЛАУ

    def select_frame_by_name(self, name):  # Выбор фрейма
        if name == "Матричный калькулятор":
            self.matrix_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.matrix_frame.grid_forget()
        if name == "Решение СЛАУ":
            self.slau_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.slau_frame.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
