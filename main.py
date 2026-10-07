import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from PIL import Image, ImageTk


WIN_RULES = {
    'rock': ['scissors'],
    'scissors': ['paper'],
    'paper': ['rock']
}
CHOICE_NAMES = {'rock': 'Камень', 'paper': 'Бумага', 'scissors': 'Ножницы'}


class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🪨Камень Ножн✂️ицы  Бумага📄")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Загружаем иконки
        self.load_images()

        # Счёт
        self.player_score = 0
        self.computer_score = 0

        # Стиль для современного вида
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 12), padding=(10, 8))
        style.configure('TLabel', font=('Segoe UI', 12))

        # === ЗАГОЛОВОК И КНОПКИ ВЫБОРА ===
        title_frame = ttk.Frame(self.root)  # Обёртка для всего верхнего блока
        title_frame.pack(pady=10)

        # Сам заголовок
        title_label = ttk.Label(title_frame, text="КНБ", 
                               font=('Segoe UI', 24, 'bold'), foreground='#2C3E50')
        title_label.pack(side='top', pady=10)

        # Блок кнопок выбора
        choices_frame = ttk.Frame(title_frame)  # Внутри обёртки, чтобы всё было по центру
        choices_frame.pack()  # Не side=left!

        for choice in ('rock', 'paper', 'scissors'):
            btn = ttk.Button(choices_frame, image=self.images[choice],
                             command=lambda c=choice: self.play_round(c),
                             width=7)  # Ширина нужна только для выравнивания
            btn.pack(side='left', padx=15)

        # === ПОЛЕ БОЯ + РЕЗУЛЬТАТ ===
        battle_frame = ttk.Frame(self.root)
        battle_frame.pack(pady=20)

        # Ход игрока
        self.player_label = ttk.Label(battle_frame, text=f"Вы: —",
                                     font=('Segoe UI', 14))
        self.player_label.grid(row=0, column=0, sticky='w')

        vs_label = ttk.Label(battle_frame, text="VS 🔥",
                             font=('Segoe UI', 16, 'bold'),
                             foreground='#FF9900')  # Оранжевый огонь
        vs_label.grid(row=0, column=1)

        # Ход компьютера
        self.computer_label = ttk.Label(battle_frame, text=f"ПК: —",
                                       font=('Segoe UI', 14))
        self.computer_label.grid(row=0, column=2, sticky='e')

        # Результат раунда
        self.result_label = ttk.Label(self.root, text="Сделайте ход!",
                                      font=('Segoe UI', 18, 'italic'),
                                      foreground='#7F8C8D')
        self.result_label.pack(pady=20)

        # Кнопка нового раунда
        self.new_round_btn = ttk.Button(
            self.root,
            text="⏭️ Новый раунд",
            command=self.reset_round,
            state='disabled',
            style='Accent.TButton'
        )
        style.configure('Accent.TButton', background='#2ECC71', foreground='white')
        self.new_round_btn.pack(pady=10)

        # === НИЖНИЙ БАР: СТАТУС И СЧЁТ ===
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill='both', expand=True)

        # Счет
        score_frame = ttk.Frame(status_bar)
        score_frame.pack(side='right', anchor='se', pady=10, padx=10)

        ttk.Label(score_frame, text="Вы:", font=('Segoe UI', 12)).pack(side='left')
        self.player_score_lbl = ttk.Label(score_frame, text="0", font=('Segoe UI', 12, 'bold'))
        self.player_score_lbl.pack(side='left')

        ttk.Label(score_frame, text=" | ПК:", font=('Segoe UI', 12)).pack(side='left')
        self.computer_score_lbl = ttk.Label(score_frame, text="0", font=('Segoe UI', 12, 'bold'))
        self.computer_score_lbl.pack(side='left')

        # Статус бар
        self.status_bar = ttk.Label(status_bar, text="Готов к игре!", relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def load_images(self):
        """Загрузка картинок"""
        size = (100, 100)
        self.images = {}

        for choice in CHOICE_NAMES.keys():
            try:
                img = Image.open(f"{choice}.png").resize(size, Image.Resampling.LANCZOS)
                self.images[choice] = ImageTk.PhotoImage(img)
            except Exception:
                print(f'Не найдена картинка {choice}.png! Будет отображаться заглушка.')
                color = '#A9A9A9' if choice == 'rock' else '#FFF' if choice == 'paper' else '#FFD700'
                img = Image.new('RGB', size, color=color)
                self.images[choice] = ImageTk.PhotoImage(img)

    def play_round(self, player_choice):
        computer_choice = random.choice(list(WIN_RULES.keys()))

        # Обновляем интерфейс
        self.player_label.config(text=f"Вы: {CHOICE_NAMES[player_choice]}")
        self.computer_label.config(text=f"ПК: {CHOICE_NAMES[computer_choice]}")

        # Логика победы
        result_text = "Ничья!"
        result_color = '#7F8C8D'
        self.status_bar.config(text="Ничья!")

        if WIN_RULES[player_choice][0] == computer_choice:
            result_text = "🎉 Вы победили!"
            result_color = '#27AE60'
            self.player_score += 1
            self.status_bar.config(text="Отличный ход!")
        elif WIN_RULES[computer_choice][0] == player_choice:
            result_text = "😢 Вы проиграли"
            result_color = '#C0392B'
            self.computer_score += 1
            self.status_bar.config(text="Попробуйте снова!")

        # Обновление счётчика
        self.player_score_lbl.config(text=str(self.player_score))
        self.computer_score_lbl.config(text=str(self.computer_score))

        # Оформление результата
        self.result_label.config(text=result_text, foreground=result_color)

        # Заблокировать выбор до следующего хода
        for child in self.root.winfo_children()[0].winfo_children():  # [0] - это верхний frame
            if isinstance(child, ttk.Frame):  # Это наш блок с тремя кнопками
                for sub_child in child.winfo_children():
                    sub_child.state(['disabled'])
        self.new_round_btn.state(['!disabled'])  # Разблокируем кнопку Нового раунда

    def reset_round(self):
        # Сброс меток
        self.player_label.config(text="Вы: —")
        self.computer_label.config(text="ПК: —")
        self.result_label.config(text="Сделайте ход!", foreground='#7F8C8D')
        self.status_bar.config(text="Ходите первым!")

        # Разблокировка кнопок
        for child in self.root.winfo_children()[0].winfo_children():  # [0] - это верхний frame
            if isinstance(child, ttk.Frame):  # Это наш блок с тремя кнопками
                for sub_child in child.winfo_children():
                    sub_child.state(['!disabled'])
        self.new_round_btn.state(['disabled'])


if __name__ == "__main__":
    root = tk.Tk()
    
    # Проверка наличия библиотеки Pillow
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror(
            "Ошибка", 
            "Библиотека Pillow не установлена.\nУстановите её командой:\npip install pillow\nи перезапустите игру."
        )
        root.destroy()
        exit()
        
    app = RPSGame(root)
    root.mainloop()