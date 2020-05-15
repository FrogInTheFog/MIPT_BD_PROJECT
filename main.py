#!/usr/bin/env python3

import sqlite3 as db

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QListWidgetItem, QFileDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

FormUI, Form = uic.loadUiType("window_ver_2.ui")

DB_PATH = "mybd2.s3db"

class Window(Form):
    def __init__(self, parent=None):
        # Инициализируем пользовательский интервейс // UI
        super(Window, self).__init__()
        self.ui = ui = FormUI()  # ui начинка окна
        ui.setupUi(self)
        # Подключение к событиям
        ui.execute_button.clicked.connect(self.__execute)
        ui.db_select_button.clicked.connect(self.__select_db)
        ui.query_history.itemDoubleClicked.connect(self.__edit)

        ui.db_current.clicked.connect(self.__select_cur_db)

        # Подключение к бд
        #self.conn = db.connect(DB_PATH)
        self.conn = db.connect(":memory:")  # Исключительно в ОЗУ

    def __del__(self):  # деструктор
        self.ui = None  # теперь будет подобрано сборщиком мусора
        # Отключение от бд
        self.conn.close()

    def __edit(self):
        item = self.ui.query_history.currentItem()
        if not item:
            return
        self.ui.query_text.setText(item.text())

    def __execute(self):
        # Вынимаем текст из edit box
        query = self.ui.query_text.text().strip()
        # Чистим edit box
        self.ui.query_text.setText("")
        # Пропускаем следующие шаги если пустой запрос
        if query == "":
            return
        # Закидываем запрос в историю
        h = self.ui.query_history
        h.addItem(query)

        # Пытаемся выполнить запрос
        cur = self.conn.cursor()
        try:  # две ветки
            cur.execute(query)
            self.conn.commit()  # сохраняем резальтат в базе
            result = cur.fetchall()
            error = None
        except Exception as exc:
            error = str(exc)
        cur.close()

        # Создаем формализованый ответ:

        # 1)Есть ошибка:
        if error is not None:
            print(error)
            result_text = f'<span style="color: red;"><b>{error}</b></span>'
        # 2) Нет ошибки но и нет результата
        else:
            if cur.description is None:
                result_text = f'Last inserted row id: {cur.lastrowid}'
            # 3) есть результат
            else:
                result_text = '<table border=1>'
                result_text += '<tr>'
                for column_description in cur.description:
                    result_text += f'<td><b>{column_description[0]}</td></b>'
                result_text += '</tr>'
                for row in result:
                    result_text += '<tr>'
                    result_text += ''.join(f'<td>{cell}</td>' for cell in row)
                    result_text += '</tr>'
                result_text += '</table>'
        # Создат виджет для нового элемента списка
        label = QLabel(result_text)
        list_item = QListWidgetItem()
        # Устонавливаем правильные размеры для этих виджетов
        label.resize(label.sizeHint())  # пересчёт размера
        list_item.setSizeHint(label.sizeHint())
        # и добовляем элементы в list
        h.addItem(list_item)
        h.setItemWidget(list_item, label)

    def __select_cur_db(self):
        # Путь запроса для нового бд
        db_pathname = DB_PATH
        print(repr(db_pathname))
        if db_pathname is None:
            return
        # Попытка подключиться к выбранно бд
        try:
            new_db_conn = db.connect(db_pathname)

        except Exception as exc:
            print("Failed to open DB:", type(exc), exc, file=sys.stderr)
        # Обновляем UI и self.conn
        self.ui.db_path.setText(db_pathname)
        old_db_conn = self.conn
        self.conn = new_db_conn
        # Закрыть соединение со старой бд коли оно было
        if old_db_conn is not None:
            return
        try:
            old_db_conn.close()
        except Exception as exc:
            print("Warning, failure while disconnecting from old DB:",
                  type(exc), exc, file=sys.stderr)

    def __select_db(self):
        # Путь запроса для нового бд
        db_pathname, _ = QFileDialog.getOpenFileName()
        print(repr(db_pathname))
        if db_pathname is None:
            return
        # Попытка подключиться к выбранно бд
        try:
            new_db_conn = db.connect(db_pathname)

        except Exception as exc:
            print("Failed to open DB:", type(exc), exc, file=sys.stderr)
        # Обновляем UI и self.conn
        self.ui.db_path.setText(db_pathname)
        old_db_conn = self.conn
        self.conn = new_db_conn
        # Закрыть соединение со старой бд коли оно было
        if old_db_conn is not None:
            return
        try:
            old_db_conn.close()
        except Exception as exc:
            print("Warning, failure while disconnecting from old DB:",
                  type(exc), exc, file=sys.stderr)

    def keyPressEvent(self, event):
        if self.ui.query_text.hasFocus():
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):  # Работать будет последовательным сравнением
                self.__execute()


if __name__ == "__main__":
    print("_____START PROGRAM_____")
    app = QApplication(sys.argv)  # экзепляр ядра приложения
    w = Window()  # экземпляр окошка
    w.show()
    sys.exit(app.exec_())  # код завершения отдаём sys
