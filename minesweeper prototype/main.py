"""
Сапёр (Minesweeper) — реализация на Python + Tkinter
Функционал:
- Новичок / Средний / Эксперт + Пользовательские размеры
- Первый клик безопасный (мины расставляются после него)
- ЛКМ — открыть, ПКМ — цикл (флаг → вопрос → пусто)
- СКМ / двойной клик — если число и рядом столько же флагов, открыть соседей
- Таймер, счётчик мин, кнопка-смайлик для сброса
- Лучшие времена сохраняются в 'saper_scores.json'
- Горячие клавиши: R для сброса, 1-3 для смены уровня

Запуск: python saper.py
Требуется: стандартная библиотека (tkinter, json, time)
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time
import json
import os

# --- Константы уровней сложности ---
DIFFICULTIES = {
    'Beginner': (9, 9, 10),
    'Intermediate': (16, 16, 40),
    'Expert': (16, 30, 99),
}
SCOREFILE = 'saper_scores.json'

# --- Вспомогательные функции ---
def load_scores():
    if os.path.exists(SCOREFILE):
        try:
            with open(SCOREFILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_scores(scores):
    with open(SCOREFILE, 'w') as f:
        json.dump(scores, f, indent=2)


class Cell:
    def __init__(self):
        self.mine = False
        self.revealed = False
        self.flag = 0  # 0 пусто, 1 флаг, 2 вопрос
        self.adj = 0   # количество мин рядом


class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title('Сапёр')
        self.scores = load_scores()
        self.create_ui()
        self.set_game(*DIFFICULTIES['Beginner'])

    def create_ui(self):
        top = tk.Frame(self.root)
        top.pack(side=tk.TOP, pady=4)

        # Счётчик мин
        self.counter_var = tk.StringVar(value='000')
        counter = tk.Label(top, text='M:', font=('Consolas', 14))
        counter.pack(side=tk.LEFT)
        counter_val = tk.Label(top, textvariable=self.counter_var, font=('Consolas', 20), width=4, relief='sunken', bd=3)
        counter_val.pack(side=tk.LEFT, padx=6)

        # Кнопка-смайлик ASCII
        self.smiley = tk.Button(top, text=':)', font=('Consolas', 14), width=3, command=self.reset_game)
        self.smiley.pack(side=tk.LEFT, padx=6)

        # Таймер
        self.timer_var = tk.StringVar(value='000')
        timer_label = tk.Label(top, text='T:', font=('Consolas', 14))
        timer_label.pack(side=tk.LEFT)
        timer_val = tk.Label(top, textvariable=self.timer_var, font=('Consolas', 20), width=4, relief='sunken', bd=3)
        timer_val.pack(side=tk.LEFT, padx=6)

        # Кнопки уровней сложности
        menu = tk.Frame(self.root)
        menu.pack(side=tk.TOP, pady=4)
        tk.Button(menu, text='Новичок', command=lambda: self.set_game(*DIFFICULTIES['Beginner'])).pack(side=tk.LEFT, padx=3)
        tk.Button(menu, text='Средний', command=lambda: self.set_game(*DIFFICULTIES['Intermediate'])).pack(side=tk.LEFT, padx=3)
        tk.Button(menu, text='Эксперт', command=lambda: self.set_game(*DIFFICULTIES['Expert'])).pack(side=tk.LEFT, padx=3)
        tk.Button(menu, text='Свои', command=self.custom_dialog).pack(side=tk.LEFT, padx=3)
        tk.Button(menu, text='Рекорды', command=self.show_scores).pack(side=tk.LEFT, padx=6)

        # Игровое поле
        self.board_frame = tk.Frame(self.root, bd=2, relief='ridge')
        self.board_frame.pack(padx=8, pady=8)

        # Привязка клавиш
        self.root.bind('<Key>', self.on_key)

    def set_game(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines_total = mines
        self.reset_board_vars()
        self.build_board()
        self.update_counter()
        self.update_timer(0)

    def reset_board_vars(self):
        self.first_click = True
        self.started = False
        self.running = False
        self.cells = [[Cell() for _ in range(self.cols)] for __ in range(self.rows)]
        self.buttons = [[None for _ in range(self.cols)] for __ in range(self.rows)]
        self.flags_left = self.mines_total
        self.revealed_count = 0
        self.start_time = None
        self.timer_job = None

    def build_board(self):
        # Очистить поле
        for w in self.board_frame.winfo_children():
            w.destroy()
        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(self.board_frame, width=2, height=1, text='█', relief='raised', font=('Consolas', 12))
                b.grid(row=r, column=c)
                b.bind('<Button-1>', lambda e, rr=r, cc=c: self.on_left(rr, cc))
                b.bind('<Button-3>', lambda e, rr=r, cc=c: self.on_right(rr, cc))
                b.bind('<Button-2>', lambda e, rr=r, cc=c: self.on_middle(rr, cc))
                b.bind('<Double-1>', lambda e, rr=r, cc=c: self.on_double(rr, cc))
                self.buttons[r][c] = b
        self.root.update_idletasks()
        self.smiley.config(text=':)' )

    def custom_dialog(self):
        rows = simpledialog.askinteger('Свои', 'Строки (9-24)', initialvalue=9, minvalue=9, maxvalue=24)
        if rows is None:
            return
        cols = simpledialog.askinteger('Свои', 'Колонки (9-30)', initialvalue=9, minvalue=9, maxvalue=30)
        if cols is None:
            return
        max_mines = rows * cols - 1
        mines = simpledialog.askinteger('Свои', f'Мины (1-{max_mines})', initialvalue=min(10, max_mines), minvalue=1, maxvalue=max_mines)
        if mines is None:
            return
        self.set_game(rows, cols, mines)

    def place_mines(self, safe_r, safe_c):
        # Разместить мины кроме клетки клика и её соседей
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        forbidden = {(safe_r, safe_c)}
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr = safe_r + dr
                cc = safe_c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    forbidden.add((rr, cc))
        available = [s for s in spots if s not in forbidden]
        mines = set(random.sample(available, self.mines_total))
        for (r, c) in mines:
            self.cells[r][c].mine = True
        # Подсчитать числа
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c].mine:
                    continue
                adj = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        rr = r + dr
                        cc = c + dc
                        if 0 <= rr < self.rows and 0 <= cc < self.cols and self.cells[rr][cc].mine:
                            adj += 1
                self.cells[r][c].adj = adj

    def on_left(self, r, c):
        if not self.running and not self.first_click:
            return
        if self.first_click:
            # Первый клик — ставим мины
            self.place_mines(r, c)
            self.first_click = False
            self.started = True
            self.running = True
            self.start_time = time.time()
            self.update_timer()
        cell = self.cells[r][c]
        if cell.revealed or cell.flag == 1:
            return
        if cell.mine:
            self.reveal_mine(r, c)
            self.game_over(False)
            return
        self.reveal_cell(r, c)
        if self.check_win():
            self.game_over(True)

    def on_right(self, r, c):
        # ПКМ — цикл метки
        cell = self.cells[r][c]
        if cell.revealed:
            return
        cell.flag = (cell.flag + 1) % 3
        b = self.buttons[r][c]
        if cell.flag == 0:
            b.config(text='█', fg='black')
            self.flags_left += 1
        elif cell.flag == 1:
            b.config(text='F', fg='red')
            self.flags_left -= 1
        else:
            b.config(text='?', fg='blue')
        self.update_counter()

    def on_middle(self, r, c):
        self.chord(r, c)

    def on_double(self, r, c):
        self.chord(r, c)

    def chord(self, r, c):
        # Если число открыто и кол-во флагов совпадает, открыть соседей
        cell = self.cells[r][c]
        if not cell.revealed or cell.adj == 0:
            return
        flags = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    if self.cells[rr][cc].flag == 1:
                        flags += 1
        if flags != cell.adj:
            return
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    if not self.cells[rr][cc].revealed and self.cells[rr][cc].flag != 1:
                        if self.cells[rr][cc].mine:
                            self.reveal_mine(rr, cc)
                            self.game_over(False)
                            return
                        self.reveal_cell(rr, cc)
        if self.check_win():
            self.game_over(True)

    def reveal_cell(self, r, c):
        # Раскрытие ячеек (с заливкой пустых)
        stack = [(r, c)]
        while stack:
            rr, cc = stack.pop()
            cell = self.cells[rr][cc]
            if cell.revealed or cell.flag == 1:
                continue
            cell.revealed = True
            b = self.buttons[rr][cc]
            b.config(relief='sunken', state='disabled')
            self.revealed_count += 1
            if cell.adj > 0:
                b.config(text=str(cell.adj), disabledforeground=self.get_color(cell.adj))
            else:
                b.config(text=' ')
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        r2, c2 = rr + dr, cc + dc
                        if 0 <= r2 < self.rows and 0 <= c2 < self.cols:
                            if not self.cells[r2][c2].revealed and not self.cells[r2][c2].mine:
                                stack.append((r2, c2))

    def reveal_mine(self, rr, cc):
        # Показать все мины и ошибки флагов
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                b = self.buttons[r][c]
                if cell.mine:
                    b.config(text='*', disabledforeground='black', relief='sunken', state='disabled')
                elif cell.flag == 1 and not cell.mine:
                    b.config(text='X', disabledforeground='red', relief='sunken', state='disabled')
        self.buttons[rr][cc].config(bg='red')

    def get_color(self, n):
        colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'darkblue',
            5: 'brown',
            6: 'cyan',
            7: 'black',
            8: 'gray'
        }
        return colors.get(n, 'black')

    def update_counter(self):
        v = max(0, self.flags_left)
        self.counter_var.set(f'{v:03d}')

    def update_timer(self, t=None):
        if t is not None:
            self.timer_var.set(f'{int(t):03d}')
            return
        if not self.running:
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_var.set(f'{elapsed:03d}')
        self.timer_job = self.root.after(1000, self.update_timer)

    def check_win(self):
        # Победа когда все кроме мин открыты
        total_cells = self.rows * self.cols
        return self.revealed_count == total_cells - self.mines_total

    def game_over(self, won):
        self.running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        if won:
            self.smiley.config(text='B)')
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            messagebox.showinfo('Победа', f'Поле очищено за {elapsed} секунд!')
            key = f'{self.rows}x{self.cols}_{self.mines_total}'
            best = self.scores.get(key)
            if best is None or elapsed < best:
                self.scores[key] = elapsed
                save_scores(self.scores)
        else:
            self.smiley.config(text='X(')
            messagebox.showinfo('Поражение', 'Вы подорвались на мине.')

    def reset_game(self):
        # Сбросить текущее поле
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.reset_board_vars()
        self.build_board()
        self.update_counter()
        self.update_timer(0)

    def show_scores(self):
        if not self.scores:
            messagebox.showinfo('Рекорды', 'Пока нет рекордов.')
            return
        lines = []
        for k, v in sorted(self.scores.items(), key=lambda x: x[0]):
            lines.append(f'{k}: {v} сек.')
        messagebox.showinfo('Рекорды', '\n'.join(lines))

    def on_key(self, event):
        k = event.char.lower()
        if k == 'r':
            self.reset_game()
        elif k in ('1', '2', '3'):
            if k == '1':
                self.set_game(*DIFFICULTIES['Beginner'])
            elif k == '2':
                self.set_game(*DIFFICULTIES['Intermediate'])
            else:
                self.set_game(*DIFFICULTIES['Expert'])


if __name__ == '__main__':
    root = tk.Tk()
    app = Minesweeper(root)
    root.mainloop()
