import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog,
                             QWidget, QVBoxLayout, QTextEdit, QHBoxLayout)
import re
from GeminyApi import request_gem
from DeepSeekApi import request_ds
from dotenv import load_dotenv
import os


class MainWindow(QMainWindow):
    def __init__(self):
        """Инициализация элементов"""
        super().__init__()
        self.file_name = ''
        self.button = QPushButton('Open txt file')
        self.text_edit0 = QTextEdit()
        self.text_edit1 = QTextEdit()
        self.text_edit2 = QTextEdit()
        self.text_edit3 = QTextEdit()
        self.initUI()
        load_dotenv()
        self.RAPID_API_KEY = os.getenv("RAPIDAPI_KEY")
        self.prompt = ''

    def initUI(self): #
        """Располажение элементов в окне"""
        self.setWindowTitle('QFileDialog')
        self.setGeometry(400, 300, 900, 500)

        # Создаём центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаём layout и кнопку
        layout = QVBoxLayout()
        self.button.clicked.connect(self.show_file_dialog)
        layout.addWidget(self.button)

        text_row_layout = QHBoxLayout()

        text_row_layout.addWidget(self.text_edit0)
        text_row_layout.addWidget(self.text_edit1)
        text_row_layout.addWidget(self.text_edit2)
        text_row_layout.addWidget(self.text_edit3)

        layout.addLayout(text_row_layout)

        central_widget.setLayout(layout)

        self.text_edit0.setPlainText("")
        self.text_edit1.setPlainText("")
        self.text_edit2.setPlainText("")
        self.text_edit3.setPlainText("")

        self.text_edit0.setReadOnly(True)
        self.text_edit1.setReadOnly(True)
        self.text_edit2.setReadOnly(True)
        self.text_edit3.setReadOnly(True)

    def show_file_dialog(self):
        """Отправка запросов и вычисление резульата при выборе файла"""
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')
        if not self.file_name.endswith('.txt'):
            self.file_name = ''
        if self.file_name:
            with open(self.file_name) as file:
                lines = [line.rstrip() for line in file]
                res = []
                self.prompt = ('В следующих строках ты получишь математические выражения.'
                          ' Получи значения выражений и выведи ответы. На одной строке один ответ. '
                          'Больше ничего. Пример: \n Входные данные \n2 + 2\n15+28\n 16/4\n '
                          'Выходные данные\n4\n43\n4. Входные данные для тебя: \n')
                for line in lines:
                    allowed_pattern = r'^[0-9+*/(). -]+$'
                    if not bool(re.fullmatch(allowed_pattern, line)):
                        continue
                    self.prompt += line + '\n'
                    try:
                        res.append(eval(line))
                    except Exception as e:
                        res.append('')
            print(res)
            res1 = request_ds(self.prompt, self.RAPID_API_KEY)
            res2 = request_gem(self.prompt, self.RAPID_API_KEY)
            self.text_edit0.setPlainText('Выражения\n' + "\n".join([str(i) for i in lines]))
            self.text_edit1.setPlainText('Вычисленные программно\n' + "\n".join([str(i) for i in res]))
            self.text_edit2.setPlainText('DeepSeek R1 Distill Qwen 32B\n' + res1)
            self.text_edit3.setPlainText('Gemini Pro AI\n' + res2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
