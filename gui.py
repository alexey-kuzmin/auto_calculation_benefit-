from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
import sys
from main import string_date_to_dt, create_all_document
from doc import create_doc


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.text_for_out = ''
        self.fio = ''
        self.benefits = []
        self.delta_dates = []
        self.name = 'файлик'

        self.btnSetDate.clicked.connect(self.add_date)  # Выполнить функцию add_date при нажатии кнопки
        self.btnClear.clicked.connect(self.clear)
        self.btnCreateDoc.clicked.connect(self.create_doc)

    def add_date(self):
        self.text_for_out += self.lineEdit_date.text() + ' - ' + self.lineEdit_sum.text() + '\n'
        self.textBrowser.setText(self.text_for_out)
        self.delta_dates.append(self.lineEdit_date.text())
        self.benefits.append(float(self.lineEdit_sum.text()))

        self.lineEdit_date.clear()


    def create_doc(self):
        self.fio = self.lineEdit_fio.text()
        # self.benefits = float(self.lineEdit_sum.text())
        # self.delta_dates = string_date_to_dt(self.text_for_out.split('\n')[:-1])
        self.delta_dates = string_date_to_dt(self.delta_dates)
        self.name = self.lineEdit_sum_2.text()

        doc = create_doc()
        create_all_document(doc, self.name, self.fio, self.benefits, self.delta_dates)

        # print(self.fio, '---', type(self.fio))
        # print(self.delta_dates, '---', type(self.delta_dates))
        # print(self.benefits, '---', type(self.benefits))

    def clear(self):
        self.textBrowser.clear()
        self.lineEdit_sum.clear()
        self.lineEdit_fio.clear()
        self.text_for_out = ''
        self.fio = ''
        self.benefits = []
        self.delta_dates = []
        self.name = 'файлик'


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == "__main__":
    main()
# pyuic5 design.ui -o design.py
# pyinstaller -F -w --onefile gui.py


    # delta_dates = ['13.05.2020—19.05.2020', '20.05.2020—02.06.2020', '03.06.2020—16.06.2020']