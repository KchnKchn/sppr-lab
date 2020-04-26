from collections import OrderedDict

from  PyQt5 import QtWidgets, QtGui
from math import sin, cos, exp
import matplotlib.pyplot as plt

from methods_impl import methods

class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__methods = OrderedDict([
                ("Метод Стронгина", methods.StronginMethod()), 
                ("Метод Пиявского", methods.PiyavskyMethod()), 
                ("Метод перебора", methods.BruteForceMethod())
            ])
        self.__curr_method = self.__methods["Метод Стронгина"]
        self.__grid = QtWidgets.QGridLayout(self)
        self.__init_title_label()
        self.__init_fx_input()
        self.__init_x_borders()
        self.__init_methods_list()
        self.__init_r_parameter()
        self.__init_e_parameter()
        self.__init_iter_parameter()
        self.__init_button()
        self.__init_x_result()
        self.__init_f_result()
        self.__init_iter_result()

    def __init_title_label(self):
        title = QtWidgets.QLabel()
        title.setText("Поиск глобального минимума функции F(x)")
        self.__grid.addWidget(title, 0, 0, 1, 2)

    def __init_fx_input(self):
        input_label = QtWidgets.QLabel()
        input_label.setText("F(x) = ")
        self.__grid.addWidget(input_label, 1, 0, 1, 1)
        self.__input_fx = QtWidgets.QLineEdit()
        self.__input_fx.setText("2*sin(3*x)+3*cos(5*x)")
        self.__grid.addWidget(self.__input_fx, 1, 1, 1, 1)

    def __init_x_borders(self):
        x_label = QtWidgets.QLabel()
        x_label.setText("x in ")
        self.__grid.addWidget(x_label, 2, 0, 1, 1)
        self.__input_x = QtWidgets.QLineEdit()
        self.__input_x.setText("-5;5")
        self.__grid.addWidget(self.__input_x, 2, 1, 1, 1)

    def __init_methods_list(self):
        methods_list = QtWidgets.QComboBox()
        methods_list.addItems(self.__methods.keys())
        methods_list.activated[str].connect(self.__connect_change_method)
        self.__grid.addWidget(methods_list, 3, 0, 1, 2)

    def __connect_change_method(self, method_name: str):
        self.__curr_method = self.__methods[method_name]

    def __init_r_parameter(self):
        r_label = QtWidgets.QLabel()
        r_label.setText("Значение параметра r")
        self.__grid.addWidget(r_label, 4, 0, 1, 1)
        self.__input_r = QtWidgets.QLineEdit()
        self.__input_r.setText("2")
        self.__grid.addWidget(self.__input_r, 4, 1, 1, 1)

    def __init_e_parameter(self):
        e_label = QtWidgets.QLabel()
        e_label.setText("Допустимая погрешность")
        self.__grid.addWidget(e_label, 5, 0, 1, 1)
        self.__input_e = QtWidgets.QLineEdit()
        self.__input_e.setText("0.001")
        self.__grid.addWidget(self.__input_e, 5, 1, 1, 1)

    def __init_iter_parameter(self):
        iter_label = QtWidgets.QLabel()
        iter_label.setText("Максимальное количество итераций")
        self.__grid.addWidget(iter_label, 6, 0, 1, 1)
        self.__input_iter = QtWidgets.QLineEdit()
        self.__input_iter.setText("1000")
        self.__grid.addWidget(self.__input_iter, 6, 1, 1, 1)

    def __init_button(self):
        button = QtWidgets.QPushButton()
        button.setText("Вычислить")
        button.clicked.connect(self.__connect_button)
        self.__grid.addWidget(button, 7, 0, 1, 2)

    def __connect_button(self):
        f_text = self.__input_fx.text().strip()
        f = lambda x: eval(f_text.replace("x", str(x)))
        left, right = [float(x) for x in self.__input_x.text().strip().split(";")]
        r = float(self.__input_r.text())
        eps = float(self.__input_e.text())
        iter = int(self.__input_iter.text())

        self.__curr_method.set_r(r)
        self.__curr_method.set_eps(eps)
        self.__curr_method.set_max_iter(iter)
        self.__curr_method.set_bounds(left, right)
        self.__curr_method.set_f(f)

        x, z, min_index, curr_iter = self.__curr_method.calculate()

        plt.close("all")
        fig, axs = plt.subplots(num="График функции F(x)")
        axs.set_xlabel("x")
        axs.set_ylabel("F(x)")
        axs.grid(True)
        axs.plot(x, z, label="F(x)")
        axs.plot(x, [z[min_index]] * len(x) , label="Точка испытания", marker="o", ls="")
        axs.legend(title="Легенда", loc="best")
        plt.show()

        self.__x_result.setText(str(x[min_index]))
        self.__f_result.setText(str(z[min_index]))
        self.__iter_result.setText(str(curr_iter))

    def __init_x_result(self):
        x_result_label = QtWidgets.QLabel()
        x_result_label.setText("Координата минимума")
        self.__grid.addWidget(x_result_label, 8, 0, 1, 1)
        self.__x_result = QtWidgets.QLineEdit()
        self.__x_result.setReadOnly(True)
        self.__grid.addWidget(self.__x_result, 8, 1, 1, 1)

    def __init_f_result(self):
        f_result_label = QtWidgets.QLabel()
        f_result_label.setText("Значение минимума")
        self.__grid.addWidget(f_result_label, 9, 0, 1, 1)
        self.__f_result = QtWidgets.QLineEdit()
        self.__f_result.setReadOnly(True)
        self.__grid.addWidget(self.__f_result, 9, 1, 1, 1)

    def __init_iter_result(self):
        iter_result_label = QtWidgets.QLabel()
        iter_result_label.setText("Количество произведенных итераций")
        self.__grid.addWidget(iter_result_label, 10, 0, 1, 1)
        self.__iter_result = QtWidgets.QLineEdit()
        self.__iter_result.setReadOnly(True)
        self.__grid.addWidget(self.__iter_result, 10, 1, 1, 1)

class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа по дисциплине \"Системы поддержки принятия решений\"")
        self.__central = MainWidget(self)
        self.setCentralWidget(self.__central)
        self.resize(self.sizeHint())