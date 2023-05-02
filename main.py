### сапёр(MINESWEEPER) BY ARYSTAN ###
import tkinter as tk
from random import shuffle
from func_find_mines import find_mines
from tkinter.messagebox import showinfo, showerror
import sys

# dictionary for button colors;
dict_btn_colors = {
    0: 'green',
    1: 'green',
    2: 'green',
    3: 'blue',
    4: 'blue',
    5: 'red',
    6: 'red',
    7: 'red',
    8: 'red'
}
# levels dictionary
levels = {
    0: [4, 4, 2],
    1: [5, 5, 3],
    2: [9, 9, 10],
    3: [15, 15, 20]
}

class Button(tk.Button):
    # make init func of our custom button, get master or window, then x and y, and ofc args kwargs
    def __init__(self, master, x, y, num, *args, **kwargs):
        # now call parent class of our Button class and initalize it by putting args like master, args and kwargs like width and font of the btn
        super(Button, self).__init__(master, *args, **kwargs)
        # now we used an init func of its parent for making our subclasses object, all init procedures are now made on our "btn" pbject of the subclass Button
        self.x = x
        self.y = y
        self.num = num
        self.mine = False
        self.open = False

    def __repr__(self):
        return f'Button: {self.x, self.y} Num: {self.num} Mine: {self.mine}'


class MineSweeper:
    window = tk.Tk()
    rows = 9
    cols = 9
    mines = 10
    game_finished = False
    difficulty = 2
    first_move = True

    def __init__(self):
        self.buttons = []
        self.found = 0
        n = 1
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                btn = Button(self.window, x=i, y=j, num=n, width=5, height=3, font="Sans")
                # so each function has its own
                # different arguments set, we use lambda so that this function is dynamic and works as a function not
                # as one premanent object only, or else the last button will change the configs of all buttons
                btn.config(command=lambda button=btn: self.button_clicked(button))
                # events for putting flags on mines you think there are on the button
                btn.bind("<Button-3>", self.put_flag)
                n += 1
                row.append(btn)
            self.buttons.append(row)

    def put_flag(self, event):
        btn = event.widget
        if btn['state'] == 'normal':
            btn.config(text='F', state='disabled', disabedforeground='red')
        elif btn['text'] == 'F':
            btn.config(text='', state='normal')

    def button_clicked(self, button):
        # if the person lost he can't click anything
        # making sure it's impossible to lose on the first move))
        if self.first_move:
            self.display_mines(button.num)
            self.set_mines_count()
            self.first_move = False

        if self.game_finished:
            return None
        if button.mine:
            button.open = True
            button.config(text='*', highlightbackground='red', disabledforeground='black')
            button.config(state='disabled')  # make sure the button can't be clicked anymore
            self.game_finished = True
            showinfo('you have lost', 'YOU LOST!')
            for i in range(self.rows):
                for j in range(self.cols):
                    btn = self.buttons[i][j]
                    if btn.mine:
                        btn.config(text='*', highlightbackground='red', disabledforeground='black', state='disabled')
        else:
            # counting the nearest mines and displaying them
            mines_count = button.mines_count
            if mines_count == 0:
                # set suitable recursion depth
                sys.setrecursionlimit(10 ** 6)
                self.dfs(button)
            else:
                button.config(text=str(mines_count), disabledforeground=dict_btn_colors[mines_count])
                self.found += 1
        button.config(state='disabled')  # make sure the button can't be clicked anymore
        button.open = True
        # check if the person won
        print(self.found)
        if self.found == (self.cols * self.rows - self.mines):
            showinfo('nothing', 'Congrats! YOU WON!')
            self.restart()

    def dfs(self, button):
        x = button.x
        y = button.y
        button.open = True
        button.config(text='0', disabledforeground='green')
        button.config(state='disabled')  # make sure the button can't be clicked anymore
        self.found += 1
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (x+i <= self.rows - 1) and (y+j <= self.cols - 1) and (y+j >= 0) and (x+i >= 0) and not self.buttons[x+i][y+j].open:
                    if self.buttons[x+i][y+j].mines_count == 0:
                        self.dfs(self.buttons[x+i][y+j])
                    else:
                        self.buttons[x+i][y+j].open = True
                        self.buttons[x+i][y+j].config(text=str(self.buttons[x+i][y+j].mines_count),
                                                      disabledforeground=dict_btn_colors[self.buttons[x+i][y+j].mines_count])
                        self.buttons[x+i][y+j].config(state='disabled')  # make sure the button can't be clicked anymore
                        self.found += 1

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        drop_down_menu = tk.Menu(menubar)
        # restart the class basically))
        drop_down_menu.add_command(label='Play again!', command=self.restart)
        drop_down_menu.add_command(label='Level', command=self.change_difficulty)
        # for quiting the game
        drop_down_menu.add_command(label='Quit', command=self.window.destroy)
        menubar.add_cascade(label='Menu', menu=drop_down_menu)

        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j, stick='NEWS')
                
        for i in range(self.rows):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(self.cols):
            tk.Grid.columnconfigure(self.window, i, weight=1)
            
    def change_difficulty(self):
        difficulty_settings = tk.Toplevel(self.window)
        difficulty_settings.wm_title('Level Selection')
        tk.Label(difficulty_settings, text='Level 0, 1, 2, or 3').grid(row=0, column=0)
        input_difficulty = tk.Entry(difficulty_settings)
        input_difficulty.grid(row=0, column=1, padx=15, pady=15)
        input_difficulty.insert(0, str(self.difficulty))
        button_save = tk.Button(difficulty_settings, text='Change!', command=lambda: self.set_difficulty(input_difficulty))
        button_save.grid(row=1, column=0, columnspan=2)

    def set_difficulty(self, difficulty: tk.Entry):
        # change the difficulty and use mod to make sure the number is in range(0, 4), not inclusive))
        try:
            difficulty = int(difficulty.get()) % 4
        # make sure user enters integer
        except:
            showerror('nothing', 'You entered a wrong value! Type in only integers...')
            return None
        self.rows = levels[difficulty][0]
        self.cols = levels[difficulty][1]
        self.mines = levels[difficulty][2]
        self.difficulty = difficulty
        self.restart()

    def restart(self):
        # delete all widgets and build them again by calling init and the start game method
        [child.destroy() for child in self.window.winfo_children()]
        self.first_move = True
        self.game_finished = False
        self.__init__()
        self.start_game()


    def start_game(self):
        self.create_widgets()
        self.window.mainloop()

    def set_mines_count(self):
        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.buttons[i][j]
                if not btn.mine:
                    mines_count = find_mines(self.buttons, btn.x, btn.y)
                    btn.mines_count = mines_count

    def print_buttons(self):
        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.buttons[i][j]
                if btn.mine:
                    print('M', end=' ')
                else:
                    print(btn.mines_count, end=' ')
            print()

    def display_mines(self, button_num):
        mines_places = self.generate_mines_pos(button_num)
        for column in self.buttons:
            for btn in column:
                if btn.num in mines_places:
                    btn.mine = True
        print(self.buttons)

    def generate_mines_pos(self, button_num):
        mines_positions = list(range(1, self.cols * self.rows + 1))
        # remove the first button which user clicked on;
        mines_positions.pop(button_num-1)
        print(mines_positions)
        shuffle(mines_positions)
        return mines_positions[:self.mines]


game = MineSweeper()
game.start_game()
game.print_buttons()
### MADE WITH LOVE, BY ARYSTAN KAIRBAYEV 23 april 2023 ###
