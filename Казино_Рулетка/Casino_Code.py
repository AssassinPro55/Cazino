from pygame import mixer
import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPalette, QBrush, QPixmap

class RouletteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.balance = 1000
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Казино: Рулетка')
        self.setGeometry(100, 100, 900, 750)
        palette = QPalette()
        background_path = "golden_background.png"
        brush = QBrush(QPixmap(background_path).scaled(self.size()))
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # Заголовок
        self.title = QLabel('Добро пожаловать в казино!', self)
        self.title.setFont(QFont('Arial', 30))

        # Баланс
        self.balance_label = QLabel(f'Ваш баланс: {self.balance} ₽', self)
        self.balance_label.setFont(QFont('Arial', 24))

        # Поле для ставки
        self.bet_label = QLabel('Ваша ставка:', self)
        self.bet_input = QLineEdit(self)
        self.bet_input.setStyleSheet("QLineEdit { padding: 6px; font-size: 28px; }")
        self.bet_label.setFont(QFont('Arial', 23))

        # Выбор типа ставки
        self.choice_label = QLabel('Выберите тип ставки:', self)
        self.choice_label.setFont(QFont('Arial', 21))

        self.even_btn = QPushButton('Чётное', self)
        self.even_btn.setFont(QFont('Arial', 21))

        self.odd_btn = QPushButton('Нечётное', self)
        self.odd_btn.setFont(QFont('Arial', 21))

        self.red_btn = QPushButton('Красное', self)
        self.red_btn.setFont(QFont('Arial', 21))
        self.red_btn.setStyleSheet("color: firebrick;")

        self.black_btn = QPushButton('Чёрное', self)
        self.black_btn.setFont(QFont('Arial', 21))
        
        # Кнопка вращения
        self.spin_btn = QPushButton('Крутить!', self)
        self.spin_btn.setFont(QFont('Arial', 21))

        # Результат
        self.result_label = QLabel('Выпало: -', self)
        self.result_label.setFont(QFont('Arial', 25))

        # Отображение типа ставки
        self.type_bet_label = QLabel('Тип ставки: -', self)
        self.type_bet_label.setFont(QFont('Arial', 25))

        # Числа красные и чёрные
        self.red_numbers = [1, 2, 4, 7, 8, 10, 13, 15, 18, 19, 21, 22, 24, 25, 29, 30, 34, 36]
        all_numbers = set(range(1, 37))
        remaining_numbers = list(all_numbers - set(self.red_numbers)) 
        random.shuffle(remaining_numbers)
        target_red_count = 18
        self.red_numbers += remaining_numbers[:target_red_count - len(self.red_numbers)]
        self.black_numbers = list(all_numbers - set(self.red_numbers))

        # Размещение элементов
        layout = QVBoxLayout()

        layout.addWidget(self.title)
        layout.addWidget(self.balance_label)

        bet_layout = QHBoxLayout()

        bet_layout.addWidget(self.bet_label)
        bet_layout.addWidget(self.bet_input)

        layout.addLayout(bet_layout)

        layout.addWidget(self.choice_label)

        choice_layout = QHBoxLayout()
        choice_layout.addWidget(self.even_btn)
        choice_layout.addWidget(self.odd_btn)
        choice_layout.addWidget(self.red_btn)
        choice_layout.addWidget(self.black_btn)

        layout.addLayout(choice_layout)
        layout.addWidget(self.spin_btn)

        low_layout = QHBoxLayout()
        layout.addLayout(low_layout)
        low_layout.addWidget(self.result_label)
        low_layout.addWidget(self.type_bet_label)

        self.setLayout(layout)

        # Музыка
        mixer.init()
        mixer.music.load('Kazino_music.mp3')
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)

        # Функции к кнопкам
        self.even_btn.clicked.connect(lambda: self.set_choice('even'))
        self.odd_btn.clicked.connect(lambda: self.set_choice('odd'))
        self.spin_btn.clicked.connect(self.spin)
        self.red_btn.clicked.connect(lambda: self.set_choice('red'))
        self.black_btn.clicked.connect(lambda: self.set_choice('black'))

    def set_choice(self, choice):
        """Устанавливает тип ставки"""
        self.choice = choice
        choice_names = {
        'even': 'Чётное',
        'odd': 'Нечётное',
        'red': 'Красное',
        'black': 'Чёрное'
        }
        self.type_bet_label.setText(f"Тип ставки: {choice_names.get(choice, '-')}")


    def spin(self):
        try:
            bet = int(self.bet_input.text())
            if bet <= 0 or bet > self.balance:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректную ставку!')
            return

        # Блокируем кнопку, чтобы не запустить игру дважды
        self.spin_btn.setEnabled(False)
        self.bet_input.setEnabled(False)
        self.even_btn.setEnabled(False)
        self.odd_btn.setEnabled(False)
        self.red_btn.setEnabled(False)
        self.black_btn.setEnabled(False)


        # --- АНИМАЦИЯ (Быстрая смена чисел) ---
        # Генерируем 2000 случайных чисел для "прокрутки"
        for _ in range(2000):
            fake_num = random.randint(0, 36)
            self.result_label.setText(f'Выпало: {fake_num}')
            # Эта строчка заставляет окно перерисоваться мгновенно
            QApplication.processEvents() 

        result = random.randint(0, 36)

        if result in self.red_numbers:
            color = 'firebrick'
            formatted_result = f"<font color='{color}'>{result}</font>"
            color_name = 'красный'

        elif result == 0:
            color = 'darkgreen'
            formatted_result = f"<font color='{color}'>{result}</font>"
            color_name = 'зелёное'

        else:
            color = 'black'
            formatted_result = f"<font color='{color}'>{result}</font>"
            color_name = 'чёрный'

        self.result_label.setText(f'Выпало: {formatted_result}')

        win = False
        if self.choice == 'even' and result % 2 == 0 and result != 0:
            win = True
            prize = bet
            msg = f'Поздравляем! Вы выиграли {prize} ₽'
            self.balance += prize
            QMessageBox.information(self, 'Победа!', msg)

        elif self.choice == 'odd' and result % 2 != 0 and result != 0:
            win = True
            prize = bet
            msg = f'Поздравляем! Вы выиграли {prize} ₽'
            self.balance += prize
            QMessageBox.information(self, 'Победа!', msg)

        elif self.choice == 'red' and result in self.red_numbers:
            win = True
            prize = bet
            self.balance += prize
            QMessageBox.information(self, 'Победа!', f'Поздравляем! Выиграл красный цвет. Ваш приз: {prize} ₽')

        elif self.choice == 'black' and result in self.black_numbers:
            win = True
            prize = bet
            self.balance += prize
            QMessageBox.information(self, 'Победа!', f'Поздравляем! Выиграл чёрный цвет. Ваш приз: {prize} ₽')

        elif result == 0:
            QMessageBox.warning(self, 'Проигрыш', 'К сожалению, вы проиграли. Выпало безвыигрышное число - 0.')

        else:
            self.balance -= bet
            QMessageBox.warning(self, 'Проигрыш', 'К сожалению, вы проиграли.')

        # Обновление баланса, поля ввода и кнопок на экране
        self.balance_label.setText(f'Ваш баланс: {self.balance} ₽')
        self.spin_btn.setEnabled(True)
        self.bet_input.setEnabled(True)
        self.even_btn.setEnabled(True)
        self.odd_btn.setEnabled(True)
        self.red_btn.setEnabled(True)
        self.black_btn.setEnabled(True)
        self.bet_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RouletteApp()
    window.show()
    sys.exit(app.exec_())