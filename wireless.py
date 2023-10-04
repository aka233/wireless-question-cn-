#! /usr/bin/python3
import re

def parse_question_data(txt_data):
    questions = []
    question_data = re.findall(r'\[I\]([^[]+)\n\[Q\]([^[]+)\n\[A\]([^[]+)\n\[B\]([^[]+)\n\[C\]([^[]+)\n\[D\]([^[]+)', txt_data)
    for item in question_data:
        question = {
            'id': item[0],
            'question': item[1],
            'options': [item[2], item[3], item[4], item[5]],
            'answer': item[2]  # All answers are fixed as item[0]
        }
        questions.append(question)
    return questions

# Load and parse question data from the file
def load_questions_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        txt_data = file.read()
    questions = parse_question_data(txt_data)
    return questions

import os
import sys
import json  # Import the json module
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtGui import QFont
class QuizApp(QWidget):
    def __init__(self, questions, randomize_options):
        super().__init__()
        self.questions = questions
        self.current_question_index = 0
        self.score = 0
        self.randomize_options = randomize_options
        self.shuffled_options = []  # Shuffled options for the current question
        self.load_user_progress()
        self.init_ui()

    def init_ui(self):
        icon_path = "icon.png"  # 替换成你的图标文件路径
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle('无线电A类题库')
        self.setGeometry(100, 100, 600, 400)

        self.question_label = QLabel()
        font1 = QFont()
        font1.setPointSize(16)  # 设置  字体大小为23
        self.question_label.setFont(font1)

        self.question_label.setWordWrap(True)

        font2=QFont()
        font2.setPointSize(14)
        
        self.option_a = QRadioButton()
        self.option_b = QRadioButton()
        self.option_c = QRadioButton()
        self.option_d = QRadioButton()

        self.option_a.setFont(font2)
        self.option_b.setFont(font2)
        self.option_c.setFont(font2)
        self.option_d.setFont(font2)


        # 允许自动换行
        self.option_a.setStyleSheet("white-space: pre-wrap;")
        self.option_b.setStyleSheet("white-space: pre-wrap;")
        self.option_c.setStyleSheet("white-space: pre-wrap;")
        self.option_d.setStyleSheet("white-space: pre-wrap;")
    


        # 设置整体窗口的样式表，将背景设置为暗色调
        self.setStyleSheet("background-color: #333; color: white;")


        self.next_button = QPushButton('下一个')

        self.next_button.clicked.connect(self.show_next_question)

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addWidget(self.option_a)
        layout.setSpacing(8)
        layout.addWidget(self.option_b)
        layout.setSpacing(8)
        layout.addWidget(self.option_c)
        layout.setSpacing(8)
        layout.addWidget(self.option_d)
        layout.addWidget(self.next_button)
        
        self.setLayout(layout)

        self.show_question(self.current_question_index)


    def shuffle_options(self):
        question = self.questions[self.current_question_index]
        self.shuffled_options = question['options'].copy()
        random.shuffle(self.shuffled_options)
        self.option_a.setText('A. ' + self.shuffled_options[0].replace('\n',''))
        self.option_b.setText('B. ' + self.shuffled_options[1].replace('\n',''))
        self.option_c.setText('C. ' + self.shuffled_options[2].replace('\n',''))
        self.option_d.setText('D. ' + self.shuffled_options[3].replace('\n',''))

    def show_question(self, index):
        question = self.questions[index]
        self.question_label.setText(f'Question {index + 1}: {question["question"]}')
        if self.randomize_options:
            self.shuffle_options()
        else:
            self.option_a.setText('A. ' + question['options'][0].replace('\n',''))
            self.option_b.setText('B. ' + question['options'][1].replace('\n',''))
            self.option_c.setText('C. ' + question['options'][2].replace('\n',''))
            self.option_d.setText('D. ' + question['options'][3].replace('\n',''))

    def show_next_question(self):

        selected_option = self.get_selected_option()
        correct_option = self.questions[self.current_question_index]['options'][0]

        if selected_option[:-1] == correct_option:
            #QMessageBox.information(self, 'Correct', 'Your answer is correct!')
            self.score += 1
        else:
            QMessageBox.information(self, 'Incorrect', f'Your answer is incorrect.\nCorrect answer is: {correct_option}')

        self.current_question_index += 1
        self.save_user_progress()
        if self.current_question_index < len(self.questions):
            self.show_question(self.current_question_index)
        else:
            QMessageBox.information(self, 'Quiz Completed', f'Quiz completed!\nYour score: {self.score}')

    def get_selected_option(self):
        if self.option_a.isChecked():
            self.option_a.setAutoExclusive(False)
            self.option_a.setChecked(False)
            self.option_a.setAutoExclusive(True)
            return self.shuffled_options[0]+'A' if randomize_options else self.questions[self.current_question_index]['options'][0]+'A'
        elif self.option_b.isChecked():
            self.option_b.setAutoExclusive(False)
            self.option_b.setChecked(False)
            self.option_b.setAutoExclusive(True)
            return self.shuffled_options[1]+'B' if randomize_options else self.questions[self.current_question_index]['options'][1]+'B'
        elif self.option_c.isChecked():
            self.option_c.setAutoExclusive(False)
            self.option_c.setChecked(False)
            self.option_c.setAutoExclusive(True)
            return self.shuffled_options[2]+'C' if randomize_options else self.questions[self.current_question_index]['options'][2]+'C'
        elif self.option_d.isChecked():
            self.option_d.setAutoExclusive(False)
            self.option_d.setChecked(False)
            self.option_d.setAutoExclusive(True)
            return self.shuffled_options[3]+'D' if randomize_options else self.questions[self.current_question_index]['options'][3]+'D'
        else:
            return ''
        

        # Save user progress to a file
    def save_user_progress(self):
        progress = {
            'current_question_index': self.current_question_index,
            'score': self.score
        }
        with open('user_progress.json', 'w') as file:
            json.dump(progress, file)


    # Load user progress from a file
    def load_user_progress(self):
        if os.path.exists('user_progress.json'):
            try:
                with open('user_progress.json', 'r') as file:
                    progress = json.load(file)
                    self.current_question_index = progress.get('current_question_index', 0)
                    self.score = progress.get('score', 0)
            except (FileNotFoundError, json.JSONDecodeError):
                # Handle the case where the file is empty or not a valid JSON
                self.current_question_index = 0
                self.score = 0
        else:
            # File doesn't exist, start fresh
            self.current_question_index = 0
            self.score = 0





if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python script.py question_file.txt (0 for in-order, 1 for randomize)')
        sys.exit(1)
    
    question_file = sys.argv[1]
    randomize_options = int(sys.argv[2]) == 1
    questions = load_questions_from_file(question_file)

    app = QApplication(sys.argv)
    quiz_app = QuizApp(questions, randomize_options)
    quiz_app.show()
    sys.exit(app.exec())
