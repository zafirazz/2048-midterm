from tkinter import Frame, Label, CENTER
import random
import functions
import visual as v

def gen():
    return random.randint(0, v.LENGTH - 1)

class Game(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('The 2048 variation')
        self.master.bind("<Key>", self.keys)

        self.commands = {
            v.UP: functions.up,
            v.DOWN: functions.down,
            v.LEFT: functions.left,
            v.RIGHT: functions.right,
            v.UP_ALT: functions.up,
            v.DOWN_ALT: functions.down,
            v.LEFT_ALT: functions.left,
            v.RIGHT_ALT: functions.right,
        }

        self.cells = []
        self.build_game()
        self.matrix = functions.creating_game(v.LENGTH)
        self.history = []
        self.draw()

        self.mainloop()

    def build_game(self):
        background = Frame(self, bg=v.BG, width=v.SIZE, height=v.SIZE)
        background.grid()

        for i in range(v.LENGTH):
            row = []
            for j in range(v.LENGTH):
                cell = Frame(
                    background,
                    bg=v.BG,
                    width=v.SIZE / v.LENGTH,
                    height=v.SIZE / v.LENGTH
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=v.GRIDS,
                    pady=v.GRIDS
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=v.BG_MP,
                    justify=CENTER,
                    font=v.FONT,
                    width=5,
                    height=2)
                t.grid()
                row.append(t)
            self.cells.append(row)

    def draw(self):
        for i in range(v.LENGTH):
            for j in range(v.LENGTH):
                new = self.matrix[i][j]
                if new == 0:
                    self.cells[i][j].configure(text="",bg=v.BG_MP)
                else:
                    self.cells[i][j].configure(
                        text=str(new),
                        bg=v.RECTANGLE_BG[new],
                        fg=v.CELL_COLOR[new])

        self.update_idletasks()

    def keys(self, event):
        key = event.keysym
        print(event)
        if key == v.KEY_EXIT:
            exit()
        if key == v.KEY_BACK and len(self.history) > 1:
            self.matrix = self.history.pop()
            self.draw()
            print('back on step total step:', len(self.history))
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = functions.another_round(self.matrix)
                self.history.append(self.matrix)
                self.draw()
                if functions.curr_state(self.matrix) == 'WIN':
                    self.cells[1][1].configure(text="CONG", bg=v.BG_MP)
                    self.cells[1][2].configure(text="RATULATIONS!", bg=v.BG_MP)
                if functions.curr_state(self.matrix) == 'LOST':
                    self.cells[1][1].configure(text="GAME", bg=v.BG_MP)
                    self.cells[1][2].configure(text="OVER!", bg=v.BG_MP)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

game = Game()