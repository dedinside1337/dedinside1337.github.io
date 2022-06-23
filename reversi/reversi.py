import tkinter
import winsound
import random
import time
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk


class Board:
    def __init__(self):
        # рисуем поле
        self.coord = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.root = tkinter.Tk()
        self.window = tkinter.Canvas(self.root, width=900, height=600)
        self.window.pack()
        self.window.create_rectangle(100, 100, 500, 500, fill='green')
        self.window.create_rectangle(600, 175, 800, 275, fill='#00bfff')
        self.message = tkinter.StringVar()
        self.skip_message = tkinter.StringVar()
        self.select_message = tkinter.StringVar()
        self.select_message.set('Select game mode')
        self.select_announcer = tkinter.Label(textvariable=self.select_message, font="Arial 14")
        self.select_announcer.place(x=80, y=520)
        self.message.set("Black's turn")
        self.end_tag = False
        self.announcer = tkinter.Label(textvariable=self.message, font="Arial 14")
        self.skip_announcer = tkinter.Label(textvariable=self.skip_message, font="Arial 12")
        self.announcer.place(x=700, y=125, anchor='center')
        self.skip_announcer.place(x=700, y=150, anchor='center')
        self.game_label = self.window.create_text(700, 50, text='Reversi', font="Verdana 25 bold")
        self.b_chip = None
        self.w_chip = None
        self.lines()
        self.ccoords()
        # словарь чтобы удалять и заменять картинки фишек
        self.chips_crds = {}
        self.chips()
        self.place_start_chip()

    def chips(self):
        # назначаем атрибуты отвечающие за фишки
        img1 = Image.open('black_chip.png').resize((50, 50))
        img2 = Image.open('white_chip.png').resize((50, 50))
        self.b_chip = ImageTk.PhotoImage(img1)
        self.w_chip = ImageTk.PhotoImage(img2)

    def lines(self):
        for i in range(1, 8):
            self.window.create_line(100 + i * 50, 100, 100 + i * 50, 500)
            self.window.create_line(100, 100 + i * 50, 500, 100 + i * 50)

    def ccoords(self):
        for i, let in enumerate(self.coord):
            self.window.create_text(80, 125 + i * 50, text=str(i + 1))
            self.window.create_text(125 + i * 50, 80, text=let)

    def place_start_chip(self):
        self.chips_crds[3, 3] = self.window.create_image((250, 250), anchor='nw', image=self.w_chip)
        self.chips_crds[4, 3] = self.window.create_image((250, 300), anchor='nw', image=self.b_chip)
        self.chips_crds[3, 4] = self.window.create_image((300, 250), anchor='nw', image=self.b_chip)
        self.chips_crds[4, 4] = self.window.create_image((300, 300), anchor='nw', image=self.w_chip)


class GameMode:
    def __init__(self):
        self.pvp = False
        self.pva = False
        self.player = -1
        self.ai_values = [
            [99, -8, 8, 6, 6, 8, -8, 99],
            [-8, -24, -4, -3, -3, -4, -24, -8],
            [8, -4, 7, 4, 4, 7, -4, 8],
            [6, -3, 4, 0, 0, 4, -3, 6],
            [6, -3, 4, 0, 0, 4, -3, 6],
            [8, -4, 7, 4, 4, 7, -4, 8],
            [-8, -24, -4, -3, -3, -4, -24, -8],
            [99, -8, 8, 6, 6, 8, -8, 99]
        ]

    def ai_move(self, paths):
        best = -99
        best_moves = []
        for i in paths:
            value = self.ai_values[i[0]][i[1]]
            if value == best:
                best_moves.append(i)
            if value > best:
                best_moves = [i]
                best = value

        if best_moves:
            return best_moves[random.randrange(len(best_moves))]
        else:
            return []

class Reversi:
    def __init__(self):
        self.end_tag = True
        self.board = Board()
        self.turn = GameMode()
        self.board_data = [[0] * 8 for i in range(8)]
        self.board_data[4][4] = self.board_data[3][3] = 1  # белые 1
        self.board_data[3][4] = self.board_data[4][3] = -1  # черные -1
        self.board.window.bind('<ButtonPress-1>', self.click)
        self.show_last_result()
        self.pvp_btn = tkinter.Button(self.board.root, background="#0000ff", foreground="#eee",
                                      font="Verdana 15 italic", text='PvP', command=self.pvp_mode)
        self.pvp_btn.place(x=250, y=510)
        self.pva_btn = tkinter.Button(self.board.root, background="#0000ff", foreground="#eee",
                                      font="Verdana 15 italic", text='PvAI', command=self.pva_mode)
        self.pva_btn.place(x=310, y=510)
        self.skip_btn = tkinter.Button(self.board.root, background="#0000ff", foreground="#eee",
                                       font="Verdana 15 italic", text='Skip turn', command=self.click_skip)
        self.skip_btn.place(x=645, y=300)

    def pvp_mode(self):
        self.turn.pvp = True
        self.pvp_btn.destroy()
        self.pva_btn.destroy()
        self.board.select_announcer.destroy()

    def pva_mode(self):
        self.turn.pva = True
        self.pvp_btn.destroy()
        self.pva_btn.destroy()
        self.board.select_announcer.destroy()

    def click(self, event):
        if 100 <= event.x <= 100 + (50 * 8) and 100 <= event.y <= 100 + (50 * 8):
            square_coords = ((event.x // 50) - 2, (event.y // 50) - 2)
            if self.turn.pvp is True or self.turn.pva is True:
                if self.check_square(square_coords) and square_coords[::-1] in self.search_paths():
                    if self.turn.player == 1:
                        chip = self.board.w_chip
                    else:
                        chip = self.board.b_chip

                    self.board.chips_crds[square_coords[1], square_coords[0]] = self.board.window.create_image(
                        ((event.x // 50) * 50, (event.y // 50) * 50), anchor='nw', image=chip)
                    self.board_data[square_coords[1]][square_coords[0]] = self.turn.player
                    winsound.PlaySound('s.wav', winsound.SND_ASYNC)
                    self.swap_chips(square_coords[::-1], chip)
                    self.swap_turn()
                    self.board.skip_message.set(' ')

                    self.end_tag = False
                if len(self.search_paths()) == 0:
                    self.board.skip_message.set('You have no moves. You should skip your turn')
                if sum(map(lambda x: x.count(0), self.board_data)) == 0:
                    self.end_game()

    def ai_click(self, move):

        if self.turn.player == 1:
            chip = self.board.w_chip
        else:
            chip = self.board.b_chip
        self.board.chips_crds[move[0], move[1]] = self.board.window.create_image(
                        (move[1] * 50 + 100, move[0] * 50 + 100), anchor='nw', image=chip)
        self.board_data[move[0]][move[1]] = self.turn.player
        winsound.PlaySound('s.wav', winsound.SND_ASYNC)
        self.swap_chips(move, chip)
        self.swap_turn()
        self.board.skip_message.set(' ')
        self.end_tag = False
        if len(self.search_paths()) == 0:
            self.board.skip_message.set('You have no moves. You should skip your turn')
        if sum(map(lambda x: x.count(0), self.board_data)) == 0:
            self.end_game()

    def swap_turn(self):
        if self.turn.player == 1:
            self.turn.player = -1
            if self.turn.pva is True:
                self.board.message.set("Player turn")
            else:
                self.board.message.set("Black's turn")
        elif self.turn.player == -1:
            self.turn.player = 1
            if self.turn.pva is True:
                self.board.message.set("Bot turn")
                move = self.turn.ai_move(self.search_paths())
                time.sleep(2)
                self.ai_click(move)
            else:
                self.board.message.set("White's turn")

    # проверяет занят ли квадрат
    def check_square(self, crds):
        if self.board_data[crds[1]][crds[0]] == 0:
            return True
        else:
            return False

    # ищет все возможные ходы
    def search_paths(self):
        valid_sqrs = []
        for i in range(8):
            for j in range(8):
                if self.path_1((i, j)) or self.path_2((i, j)) or self.path_3((i, j)) or \
                        self.path_4((i, j)) or self.path_5((i, j)) or self.path_6((i, j)) or \
                        self.path_7((i, j)) or self.path_8((i, j)):
                    if self.board_data[i][j] == 0:
                        valid_sqrs.append((i, j))
        return valid_sqrs

    def path_1(self, crds):
        valid = False
        if crds[0] > 0 and crds[1] > 0:
            dist = (crds[0], crds[1])[crds[0] > crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] - i][crds[1] - i] == self.turn.player * (-1):
                    valid = True
                    continue
                elif self.board_data[crds[0] - i][crds[1] - i] == 0:
                    return False
                else:
                    if valid:
                        return True
                    return False
        return False

    def path_2(self, crds):
        valid = False
        dist = crds[0]
        for i in range(1, dist + 1):
            if self.board_data[crds[0] - i][crds[1]] == self.turn.player * (-1):
                valid = True
                continue
            elif self.board_data[crds[0] - i][crds[1]] == 0:
                return False
            else:
                if valid:
                    return True
                return False
        return False

    def path_3(self, crds):
        valid = False
        if crds[0] > 0 and 7 - crds[1] > 0:
            dist = (crds[0], 7 - crds[1])[crds[0] > 7 - crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] - i][crds[1] + i] == self.turn.player * (-1):
                    valid = True
                    continue
                elif self.board_data[crds[0] - i][crds[1] + i] == 0:
                    return False
                else:
                    if valid:
                        return True
                    return False
        return False

    def path_4(self, crds):
        valid = False
        dist = 7 - crds[1]
        for i in range(1, dist + 1):
            if self.board_data[crds[0]][crds[1] + i] == self.turn.player * (-1):
                valid = True
                continue
            elif self.board_data[crds[0]][crds[1] + i] == 0:
                return False
            else:
                if valid:
                    return True
                return False
        return False

    def path_5(self, crds):
        valid = False
        if 7 - crds[0] > 0 and 7 - crds[1] > 0:
            dist = (7 - crds[0], 7 - crds[1])[7 - crds[0] > 7 - crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] + i][crds[1] + i] == self.turn.player * (-1):
                    valid = True
                    continue
                elif self.board_data[crds[0] + i][crds[1] + i] == 0:
                    return False
                else:
                    if valid:
                        return True
                    return False
        return False

    def path_6(self, crds):
        valid = False
        dist = 7 - crds[0]
        for i in range(1, dist + 1):
            if self.board_data[crds[0] + i][crds[1]] == self.turn.player * (-1):
                valid = True
                continue
            elif self.board_data[crds[0] + i][crds[1]] == 0:
                return False
            else:
                if valid:
                    return True
                return False
        return False

    def path_7(self, crds):
        valid = False
        if 7 - crds[0] > 0 and crds[1] > 0:
            dist = (7 - crds[0], crds[1])[7 - crds[0] > crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] + i][crds[1] - i] == self.turn.player * (-1):
                    valid = True
                    continue
                elif self.board_data[crds[0] + i][crds[1] - i] == 0:
                    return False
                else:
                    if valid:
                        return True
                    return False
        return False

    def path_8(self, crds):
        valid = False
        dist = crds[1]
        for i in range(1, dist + 1):
            if self.board_data[crds[0]][crds[1] - i] == self.turn.player * (-1):
                valid = True
                continue
            elif self.board_data[crds[0]][crds[1] - i] == 0:
                return False
            else:
                if valid:
                    return True
                return False
        return False

    # замена фишек на другой цвет
    def swap_chips(self, crds, chip):
        if self.path_1(crds):
            dist = (crds[0], crds[1])[crds[0] > crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] - i][crds[1] - i] == self.turn.player * (-1):
                    self.board_data[crds[0] - i][crds[1] - i] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0] - i, crds[1] - i])
                    self.board.chips_crds[crds[0] - i, crds[1] - i] = self.board.window.create_image(
                        ((crds[1] - i) * 50 + 100, ((crds[0] - i) * 50) + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_2(crds):
            dist = crds[0]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] - i][crds[1]] == self.turn.player * (-1):
                    self.board_data[crds[0] - i][crds[1]] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0] - i, crds[1]])
                    self.board.chips_crds[crds[0] - i, crds[1]] = self.board.window.create_image(
                        (crds[1] * 50 + 100, (crds[0] - i) * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_3(crds):
            dist = (crds[0], 7 - crds[1])[crds[0] > 7 - crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] - i][crds[1] + i] == self.turn.player * (-1):
                    self.board_data[crds[0] - i][crds[1] + i] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0] - i, crds[1] + i])
                    self.board.chips_crds[crds[0] - i, crds[1] + i] = self.board.window.create_image(
                        ((crds[1] + i) * 50 + 100, (crds[0] - i) * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_4(crds):
            dist = 7 - crds[1]
            for i in range(1, dist + 1):
                if self.board_data[crds[0]][crds[1] + i] == self.turn.player * (-1):
                    self.board_data[crds[0]][crds[1] + i] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0], crds[1] + i])
                    self.board.chips_crds[crds[0], crds[1] + i] = self.board.window.create_image(
                        ((crds[1] + i) * 50 + 100, crds[0] * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_5(crds):
            dist = (7 - crds[0], 7 - crds[1])[7 - crds[0] > 7 - crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] + i][crds[1] + i] == self.turn.player * (-1):
                    self.board_data[crds[0] + i][crds[1] + i] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0] + i, crds[1] + i])
                    self.board.chips_crds[crds[0] + i, crds[1] + i] = self.board.window.create_image(
                        ((crds[1] + i) * 50 + 100, (crds[0] + i) * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_6(crds):
            dist = 7 - crds[0]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] + i][crds[1]] == self.turn.player * (-1):
                    self.board_data[crds[0] + i][crds[1]] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0] + i, crds[1]])
                    self.board.chips_crds[crds[0] + i, crds[1]] = self.board.window.create_image(
                        (crds[1] * 50 + 100, (crds[0] + i) * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_7(crds):
            dist = (7 - crds[0], crds[1])[7 - crds[0] > crds[1]]
            for i in range(1, dist + 1):
                if self.board_data[crds[0] + i][crds[1] - i] == self.turn.player * (-1):
                    self.board_data[crds[0] + i][crds[1] - i] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0] + i, crds[1] - i])
                    self.board.chips_crds[crds[0] + i, crds[1] - i] = self.board.window.create_image(
                        ((crds[1] - i) * 50 + 100, (crds[0] + i) * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break
        if self.path_8(crds):
            dist = crds[1]
            for i in range(1, dist + 1):
                if self.board_data[crds[0]][crds[1] - i] == self.turn.player * (-1):
                    self.board_data[crds[0]][crds[1] - i] = self.turn.player
                    self.board.window.delete(self.board.chips_crds[crds[0], crds[1] - i])
                    self.board.chips_crds[crds[0], crds[1] - i] = self.board.window.create_image(
                        ((crds[1] - i) * 50 + 100, crds[0] * 50 + 100), anchor='nw', image=chip)
                    self.board.window.update()
                    self.board.window.after(100)
                else:
                    break

    def click_skip(self):
        if len(self.search_paths()) == 0:
            self.swap_turn()
            self.end_tag = True
            self.board.skip_message.set(' ')
        else:
            self.board.skip_message.set('You still have moves')
        if len(self.search_paths()) == 0 and self.end_tag is True:
            self.end_game()

    def end_game(self):
        res_b, res_w = 0, 0
        for i in range(8):
            for j in range(8):
                if self.board_data[i][j] == -1:
                    res_b += 1
                if self.board_data[i][j] == 1:
                    res_w += 1
        if res_w > res_b:
            end_message = "Game over. White win"
        elif res_w < res_b:
            end_message = "Game over. Black win"
        else:
            end_message = 'Game over. Draw'
        self.result(res_b, res_w, end_message)
        self.fireworks()
        msg_box = tkinter.messagebox.askyesno('Game Over',
                                              end_message + f'\n Result: B-{res_b},W-{res_w}' + '\n Try again?')
        if msg_box:
            self.board.root.destroy()
            Game()
        else:
            self.board.root.destroy()

    def show_last_result(self):
        with open('result.txt', 'r') as file:
            f = file.readlines()
            result = f[-4] + f[-3] + f[-2]
        self.board.window.create_text(700, 190, font="Verdana 12 italic", text='Last game')
        self.board.window.create_text(605, 210, font="Verdana 10", anchor='nw', text=result)

    def fireworks(self):
        for i in range(9):
            img_path = f"fireworks\\{i}.png"
            fw_image = ImageTk.PhotoImage(file=img_path)
            self.board.window.create_image(450, 300, image=fw_image)
            self.board.window.update()
            self.board.window.after(80)

    @staticmethod
    def result(black, white, msg):
        date = datetime.now()
        with open('result.txt', 'a') as file:
            file.write(
                '\n' + str(date)[
                       :-7] + '\n' + msg + f'\nResult Black: {black}, White: {white}\n---------------------------\n')


class Game(Reversi):
    def __init__(self):
        super().__init__()
        tkinter.mainloop()


Game()
