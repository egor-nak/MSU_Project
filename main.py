import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QCheckBox, QBoxLayout
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIntValidator
from random import randrange
import time
from datetime import datetime
import numpy as np
import pandas as pd
import pyqtgraph as pg

SCREEN_SIZE = [1000, 700]

sz_to_num = {"0.2": 1,
             "0.5": 2,
             "0.7": 3}


class main_window(QWidget):
    def __init__(self):
        super().__init__()

        # Second page

        self.patient_answers = None
        self.iteration_count = None
        self.stairs_mode_on = None
        self.pressure_gramms = None
        self.name_of_patient_final = None
        self.input_force_of_preassure = None
        self.force_of_preassure = None
        self.save_protocole_btn = None
        self.delete_last_elem_from_sequence_btn = None
        self.add_07_pin_title = None
        self.add_07_pin_btn = None
        self.add_05_pin_title = None
        self.add_05_pin_btn = None
        self.add_02_pin_title = None
        self.add_02_pin_btn = None
        self.stairs_algorithm_status = None
        self.sequence_of_pins = None
        self.sequence_of_pins_title = None
        self.input_name_patient = None
        self.name_patient = None
        self.testing_protocole_title = None

        self.image_logo_brain_not_main = None

        self.sequence_of_pins_that_goes_to_arduino = []
        self.save_protocole_btn_size = [220, 50]

        # Первая страница

        self.pixmap_logo_brain_not_main = None

        self.start_btn = None
        self.author_name = None
        self.main_name = None
        self.image_logo_brain = None
        self.pixmap_logo_brain = None
        self.logo_brain_size = [150, 150]
        self.start_btn_size = [200, 50]
        self.logo_brain_not_main_size = [100, 100]
        self.objects_from_main_page = [self.start_btn, self.author_name, self.main_name, self.image_logo_brain]
        self.main_window()

    def main_window(self):
        self.setGeometry(250, 50, *SCREEN_SIZE)
        self.setWindowTitle('Neuro MSU')
        self.setWindowIcon(
            QtGui.QIcon("images/brain_logo.png"))  # авторство иконки https://www.flaticon.com/authors/vitaly-gorbachev

        # Лого на главной странице
        self.pixmap_logo_brain = QPixmap("images/brain_logo.png")
        self.pixmap_logo_brain = self.pixmap_logo_brain.scaled(*self.logo_brain_size)
        self.image_logo_brain = QLabel(self)
        self.image_logo_brain.setPixmap(self.pixmap_logo_brain)
        self.image_logo_brain.move((SCREEN_SIZE[0] // 2) - self.logo_brain_size[0] // 2, int(SCREEN_SIZE[1] * 0.05))

        # Название

        font_for_main_name = QtGui.QFont('Tahoma', 64)
        font_for_main_name.setBold(True)
        self.main_name = QLabel(self)
        self.main_name.setText("NEURO MSU PROJECT")
        self.main_name.setFont(font_for_main_name)
        # self.main_name.move((SCREEN_SIZE[0] // 2) - self.logo_brain_size[0] // 2, int(SCREEN_SIZE[0] * 0.01))
        self.main_name.move(170, int(SCREEN_SIZE[1] * 0.05) + 125 + 20)

        # Имя автора логотипа
        self.author_name = QLabel(self)
        self.author_name.setText(
            "Автор логотипа: Vitaly Gorbachev Link: https://www.flaticon.com/authors/vitaly-gorbachev")
        self.author_name.move(0, int(SCREEN_SIZE[1] * 0.96))

        # Кнопка начала тестипрованяи
        self.start_btn = QPushButton("Начать", self)
        font_for_start_btn = QtGui.QFont('Tahoma', 21)
        self.start_btn.setFont(font_for_start_btn)
        self.start_btn.setStyleSheet("border : 2px solid white; border-radius : 20px; background-color: white")
        self.start_btn.resize(*self.start_btn_size)
        self.start_btn.move((SCREEN_SIZE[0] // 2) - self.start_btn_size[0] // 2, int(SCREEN_SIZE[1] * 0.55))
        self.start_btn.clicked.connect(self.setting_testing_protocole_window)

    def setting_testing_protocole_window(self):
        self.sequence_of_pins_that_goes_to_arduino.clear()
        self.hide_objects_from_main_window()

        # Верхняя надпись
        font_for_testing_protocole_title = QtGui.QFont('Tahoma', 32)
        font_for_testing_protocole_title.setBold(True)
        font_for_testing_protocole_title.setUnderline(True)
        self.testing_protocole_title = QLabel(self)
        self.testing_protocole_title.setText("Протокол тестирования:")
        self.testing_protocole_title.setFont(font_for_testing_protocole_title)
        self.testing_protocole_title.show()
        self.testing_protocole_title.move(20, int(SCREEN_SIZE[1] * 0.03))

        # Логотип сверху

        self.pixmap_logo_brain_not_main = QPixmap("images/brain_logo.png")
        self.pixmap_logo_brain_not_main = self.pixmap_logo_brain_not_main.scaled(*self.logo_brain_not_main_size)
        self.image_logo_brain_not_main = QLabel(self)
        self.image_logo_brain_not_main.setPixmap(self.pixmap_logo_brain_not_main)
        self.image_logo_brain_not_main.move(SCREEN_SIZE[0] - self.logo_brain_not_main_size[0] - 25,
                                            int(SCREEN_SIZE[1] * 0.01))
        self.image_logo_brain_not_main.show()

        # Надпись "Имя пациента"

        font_for_name_patient = QtGui.QFont('Tahoma', 24)
        self.name_patient = QLabel(self)
        self.name_patient.setText("Имя пациента: ")
        self.name_patient.setFont(font_for_name_patient)
        # self.main_name.move((SCREEN_SIZE[0] // 2) - self.logo_brain_size[0] // 2, int(SCREEN_SIZE[0] * 0.01))
        self.name_patient.move(20, int(SCREEN_SIZE[1] * 0.15))
        self.name_patient.show()

        # Поле для ввода текста

        self.input_name_patient = QLineEdit(self)
        self.input_name_patient.move(self.name_patient.pos().x() + self.name_patient.size().width() + 20,
                                     self.name_patient.pos().y() + 2)
        self.input_name_patient.resize(self.input_name_patient.size().width() + 100,
                                       self.input_name_patient.size().height())
        self.input_name_patient.show()
        # print(self.name_patient.size().height())

        # Надпись Силы нажатия
        font_for_force_of_presssure = QtGui.QFont('Tahoma', 24)
        self.force_of_preassure = QLabel(self)
        self.force_of_preassure.setText("Сила нажатия граммы: ")
        self.force_of_preassure.setFont(font_for_force_of_presssure)
        self.force_of_preassure.move(self.input_name_patient.pos().x() + self.input_name_patient.size().width() + 30,
                                     int(SCREEN_SIZE[1] * 0.15))
        self.force_of_preassure.show()

        # Поле для ввода силы нажатия

        self.input_force_of_preassure = QLineEdit(self)
        self.input_force_of_preassure.setValidator(QIntValidator())
        self.input_force_of_preassure.move(
            self.force_of_preassure.pos().x() + self.force_of_preassure.size().width() + 20,
            self.force_of_preassure.pos().y() + 2)
        self.input_force_of_preassure.resize(self.input_force_of_preassure.size().width() + 100,
                                             self.input_force_of_preassure.size().height())
        self.input_force_of_preassure.show()

        # Отображение надписи "Порядок пинов"

        font_for_sequence_of_pins_title = QtGui.QFont('Tahoma', 24)
        self.sequence_of_pins_title = QLabel(self)
        self.sequence_of_pins_title.setText("Порядок пинов: ")
        self.sequence_of_pins_title.setFont(font_for_sequence_of_pins_title)
        self.sequence_of_pins_title.move(20, int(SCREEN_SIZE[1] * 0.29))
        self.sequence_of_pins_title.show()

        # Отображение последовательности пинов

        self.sequence_of_pins = QLineEdit(self)
        self.sequence_of_pins.move(self.input_name_patient.pos().x(),
                                   self.sequence_of_pins_title.pos().y() + 2)
        self.sequence_of_pins.resize(self.sequence_of_pins.size().width() + 100,
                                     self.sequence_of_pins.size().height())
        self.sequence_of_pins.setReadOnly(True)
        self.sequence_of_pins.show()

        # Checkbox алгоритма для выбора Алгоритма Лесенки

        font_for_stairs_algorithm_status = QtGui.QFont('Tahoma', 24)
        self.stairs_algorithm_status = QCheckBox(self)
        self.stairs_algorithm_status.setFont(font_for_stairs_algorithm_status)
        self.stairs_algorithm_status.setText("Использовать алгоритм Лесенки")
        self.stairs_algorithm_status.move(self.sequence_of_pins.pos().x() + self.sequence_of_pins.size().width() + 70,
                                          self.sequence_of_pins.pos().y())
        self.stairs_algorithm_status.show()

        # Button to delete elems from sequence

        font_for_delete_last_elem_from_sequence_btn = QtGui.QFont('Tahoma', 24)
        self.delete_last_elem_from_sequence_btn = QPushButton(self)
        self.delete_last_elem_from_sequence_btn.setText("-")
        self.delete_last_elem_from_sequence_btn.setFont(font_for_delete_last_elem_from_sequence_btn)
        self.delete_last_elem_from_sequence_btn.resize(39, 32)
        self.delete_last_elem_from_sequence_btn.move(
            self.sequence_of_pins.pos().x() + self.sequence_of_pins.size().width() + 20,
            self.sequence_of_pins.pos().y())
        self.delete_last_elem_from_sequence_btn.clicked.connect(self.delete_last_elem_from_sequence)
        self.delete_last_elem_from_sequence_btn.show()

        # Button for saving protocole

        font_for_save_protocole_btn = QtGui.QFont('Tahoma', 21)
        self.save_protocole_btn = QPushButton("Сохранить и начать", self)
        self.save_protocole_btn.setFont(font_for_save_protocole_btn)
        self.save_protocole_btn.setStyleSheet("border : 2px solid white; border-radius : 20px; background-color: white")
        self.save_protocole_btn.resize(*self.save_protocole_btn_size)
        self.save_protocole_btn.move((SCREEN_SIZE[0] // 2) - self.start_btn_size[0] // 2, int(SCREEN_SIZE[1] * 0.87))
        self.save_protocole_btn.clicked.connect(self.testing_patient_window)
        self.save_protocole_btn.show()

        # Buttons for adding pins

        font_for_plus_buttons_and_titles = QtGui.QFont('Tahoma', 24)

        # Setting 0.2 Button

        self.add_02_pin_btn = QPushButton(self)
        self.add_02_pin_btn.setText("+")
        self.add_02_pin_btn.setFont(font_for_plus_buttons_and_titles)
        self.add_02_pin_btn.resize(39, 32)
        self.add_02_pin_btn.move(self.sequence_of_pins_title.pos().x() - 5, self.sequence_of_pins_title.pos().y() + 50)
        self.add_02_pin_btn.clicked.connect(self.add_02_elem_into_secuence)
        self.add_02_pin_btn.show()

        self.add_02_pin_title = QLabel(self)
        self.add_02_pin_title.setFont(font_for_plus_buttons_and_titles)
        self.add_02_pin_title.move(self.add_02_pin_btn.pos().x() + self.add_02_pin_btn.size().width() + 10,
                                   self.add_02_pin_btn.pos().y())
        self.add_02_pin_title.setText("0.2 мм")
        self.add_02_pin_title.show()

        # Setting 0.5 Button

        self.add_05_pin_btn = QPushButton(self)
        self.add_05_pin_btn.setText("+")
        self.add_05_pin_btn.setFont(font_for_plus_buttons_and_titles)
        self.add_05_pin_btn.resize(39, 32)
        self.add_05_pin_btn.move(self.add_02_pin_btn.pos().x(), self.add_02_pin_btn.pos().y() + 50)
        self.add_05_pin_btn.clicked.connect(self.add_05_elem_into_secuence)
        self.add_05_pin_btn.show()

        self.add_05_pin_title = QLabel(self)
        self.add_05_pin_title.setFont(font_for_plus_buttons_and_titles)
        self.add_05_pin_title.move(self.add_05_pin_btn.pos().x() + self.add_05_pin_btn.size().width() + 10,
                                   self.add_05_pin_btn.pos().y())
        self.add_05_pin_title.setText("0.5 мм")
        self.add_05_pin_title.show()

        # Setting 0.7 Button

        self.add_07_pin_btn = QPushButton(self)
        self.add_07_pin_btn.setText("+")
        self.add_07_pin_btn.setFont(font_for_plus_buttons_and_titles)
        self.add_07_pin_btn.resize(39, 32)
        self.add_07_pin_btn.move(self.add_05_pin_btn.pos().x(), self.add_05_pin_btn.pos().y() + 50)
        self.add_07_pin_btn.clicked.connect(self.add_07_elem_into_secuence)
        self.add_07_pin_btn.show()

        self.add_07_pin_title = QLabel(self)
        self.add_07_pin_title.setFont(font_for_plus_buttons_and_titles)
        self.add_07_pin_title.move(self.add_07_pin_btn.pos().x() + self.add_07_pin_btn.size().width() + 10,
                                   self.add_07_pin_btn.pos().y())
        self.add_07_pin_title.setText("0.7 мм \n и.т.д")
        self.add_07_pin_title.show()

    def testing_patient_window(self):
        self.hide_objects_from_protocol_settings_page()
        self.name_of_patient_final = self.input_name_patient.text()
        self.pressure_gramms = self.input_force_of_preassure.text()
        self.stairs_mode_on = self.stairs_algorithm_status.isChecked()
        print(self.name_of_patient_final, self.pressure_gramms, self.stairs_mode_on)

        # Кнопка параллельно
        self.parallel_button = QPushButton(self)
        self.parallel_button.setText("Параллельно")
        self.parallel_button.resize(300, 400)
        self.parallel_button.move(SCREEN_SIZE[0] // 2 - 300, SCREEN_SIZE[1] // 2 - 200)
        self.parallel_button.show()

        # Кнопка перпендикулярно

        self.perpendicular_button = QPushButton(self)
        self.perpendicular_button.setText("Перпендикулярно")
        self.perpendicular_button.resize(300, 400)
        self.perpendicular_button.move(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 200)
        self.perpendicular_button.show()

        # Номер итерации

        font_for_iteration_number = QtGui.QFont('Tahoma', 32)
        font_for_iteration_number.setBold(True)
        self.iteration_count = QLabel(self)
        self.iteration_count.setText("Итерация 0/" + str(len(self.sequence_of_pins_that_goes_to_arduino)))
        self.iteration_count.setFont(font_for_iteration_number)
        self.iteration_count.move(SCREEN_SIZE[0] // 2 - self.iteration_count.size().width(), int(SCREEN_SIZE[1] * 0.05))
        self.iteration_count.show()

        self.patient_answers = []

        count_iteration = 0

        # Здесь должна быть пережача данных на Arduino о  силе нажатия и
        for pin in self.sequence_of_pins_that_goes_to_arduino:
            count_iteration += 1
            # пердаём данные на arduino о пине, который сечас должен использоваться
            self.iteration_count.setText(
                "Итерация " + str(count_iteration) + "/" + str(len(self.sequence_of_pins_that_goes_to_arduino)))
            tmp_patient_ans = int(randrange(2))  # 1 - верно, 0 - не верно
            self.patient_answers.append([tmp_patient_ans, pin])

        self.final_result_window()

    def final_result_window(self):
        self.hide_objects_from_testing_page()

        # Плотим психометрическую кривую

        self.plot = pg.plot()
        scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(30, 255, 35, 255))
        x_data = []
        y_data = []
        convert_answers = {}
        self.patient_answers.sort(key=lambda x: float(x[1]))
        for i in self.patient_answers:
            if i[1] in convert_answers.keys():
                convert_answers[i[1]][0] += i[0]
                convert_answers[i[1]][1] += 1
            else:
                convert_answers[i[1]] = [i[0], 1]

        for j in convert_answers.keys():
            x_data.append(float(j))
            y_data.append(convert_answers[j][0] / convert_answers[j][1])\

        print(x_data, y_data)

        scatter.setData(x_data, y_data)

        self.plot.plot(x_data, y_data, pen ='g', symbol ='x', symbolPen ='g',
                          symbolBrush = 0.2, name ='green')

        # Конвертируем данные в csv

        fl_to_csv = np.array([[self.name_patient, self.pressure_gramms]] + self.patient_answers)
        DF = pd.DataFrame(fl_to_csv)
        DF.to_csv("result.csv")

        # Отображаем csv в приложении













    def add_02_elem_into_secuence(self):
        self.sequence_of_pins_that_goes_to_arduino.append("0.2")
        self.sequence_of_pins.setText("; ".join(self.sequence_of_pins_that_goes_to_arduino))

    def add_05_elem_into_secuence(self):
        self.sequence_of_pins_that_goes_to_arduino.append("0.5")
        self.sequence_of_pins.setText("; ".join(self.sequence_of_pins_that_goes_to_arduino))

    def add_07_elem_into_secuence(self):
        self.sequence_of_pins_that_goes_to_arduino.append("0.7")
        self.sequence_of_pins.setText("; ".join(self.sequence_of_pins_that_goes_to_arduino))

    def delete_last_elem_from_sequence(self):
        if len(self.sequence_of_pins_that_goes_to_arduino) == 0:
            return
        self.sequence_of_pins_that_goes_to_arduino.pop()
        self.sequence_of_pins.setText("; ".join(self.sequence_of_pins_that_goes_to_arduino))

    def hide_objects_from_main_window(self):
        for item in [self.start_btn, self.main_name, self.image_logo_brain]:
            item.hide()

    def show_objects_from_main_window(self):
        for item in [self.start_btn, self.main_name, self.image_logo_brain]:
            item.show()

    def hide_objects_from_protocol_settings_page(self):
        for item in [self.save_protocole_btn, self.delete_last_elem_from_sequence_btn, self.add_07_pin_title,
                     self.add_07_pin_btn, self.add_05_pin_title,
                     self.add_05_pin_btn, self.add_02_pin_title,
                     self.add_02_pin_btn, self.stairs_algorithm_status,
                     self.sequence_of_pins, self.sequence_of_pins_title,
                     self.input_name_patient, self.name_patient, self.testing_protocole_title,
                     self.input_force_of_preassure, self.force_of_preassure]:
            item.hide()

    def show_objects_from_protocol_settings_page(self):
        for item in [self.save_protocole_btn, self.delete_last_elem_from_sequence_btn, self.add_07_pin_title,
                     self.add_07_pin_btn, self.add_05_pin_title,
                     self.add_05_pin_btn, self.add_02_pin_title,
                     self.add_02_pin_btn, self.stairs_algorithm_status,
                     self.sequence_of_pins, self.sequence_of_pins_title,
                     self.input_name_patient, self.name_patient, self.testing_protocole_title,
                     self.input_force_of_preassure, self.force_of_preassure]:
            item.show()

    def hide_objects_from_testing_page(self):
        for item in [self.parallel_button, self.perpendicular_button, self.iteration_count]:
            item.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    sys.exit(app.exec())
