import tkinter
from tkinter import Canvas, Label, Tk, StringVar, PhotoImage, Frame
from tkinter import messagebox
from random import choice
from collections import Counter


def check_shape(self, shape, kuroojyo, mushi, syogun, murasaki, tonakai, ryu, akanin):
    if shape is "kuroojyo":
        self.image = kuroojyo
    elif shape is "syogun":
        self.image = syogun
    elif shape is "murasaki":
        self.image = murasaki
    elif shape is "mushi":
        self.image = mushi
    elif shape is "tonakai":
        self.image = tonakai
    elif shape is "ryu":
        self.image = ryu
    elif shape is "akanin":
        self.image = akanin

class Game():
    WIDTH = 400
    HEIGHT = 600
    SIDE = 200
    NEXT_HEIGHT = 200
    SHAPES = (
        ("kuroojyo", (0, 0), (1, 0), (0, 1), (1, 1)),  # square
        ("syogun", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
        ("murasaki", (2, 0), (0, 1), (1, 1), (2, 1)),  # right el
        ("mushi", (0, 0), (0, 1), (1, 1), (2, 1)),  # left el
        ("tonakai", (0, 1), (1, 1), (1, 0), (2, 0)),  # right wedge
        ("ryu", (0, 0), (1, 0), (1, 1), (2, 1)),  # left wedge
        ("akanin", (1, 0), (0, 1), (1, 1), (2, 1)),  # symmetrical wedge
    )

    def start(self):

        def raise_frame(frame):
            frame.tkraise()
            self.timer()

        self.level = 1
        self.score = 0
        self.speed = 500
        self.counter = 0
        self.create_new_game = True

        self.root = Tk()
        self.root.title("パズルゲーム")

        # パズル画像のオブジェクトを作る
        self.kuroojyo = PhotoImage(file="./images/kuroojyo.png")
        self.mushi = PhotoImage(file="./images/mushi.png")
        self.syogun = PhotoImage(file="./images/syogun.png")
        self.murasaki = PhotoImage(file="./images/murasaki.png")
        self.tonakai = PhotoImage(file="./images/tonakai.png")
        self.ryu = PhotoImage(file="./images/ryu.png")
        self.akanin = PhotoImage(file="./images/akanin.png")
        # 落ちてくるブロックと次に落ちてくるブロックを作る
        self.first_shape = choice(self.SHAPES)
        self.second_shape = choice(self.SHAPES)


        self.start_frame = Frame(self.root, width=400, height=600)
        self.start_frame.grid(row=0, column=0, sticky='news')

        self.main_frame = Frame(self.root, width=400, height=600)
        self.main_frame.grid(row=0, column=0, sticky='news')

        self.start_frame.tkraise()

        # スタート画面作成
        status_var = StringVar()
        status_var.set("パズルゲーム")
        start_label = Label(self.start_frame, textvariable=status_var, font=("Helvetica", 30, "bold"), bg='orange')
        start_label.place(x=200, y=130)
        # ボタン
        start_btn = tkinter.Button(self.start_frame, text='開始', bg='orange', command=lambda: raise_frame(self.main_frame))

        start_btn.place(x=300, y=300)

        self.canvas = Canvas(
            self.main_frame,
            width=Game.WIDTH,
            height=Game.HEIGHT)
        self.canvas.pack(fill='both', side='left')

        self.root.bind("<Key>", self.handle_events)

        self.game_frame = Frame(self.main_frame, width=Game.SIDE, height=500, bg='orange')
        self.game_frame.pack(fill='both', side='right')

        self.status_var = StringVar()
        self.status_var.set("Level: 1, Score: 0")
        self.status = Label(self.game_frame,
                            textvariable=self.status_var,
                            font=("Helvetica", 10, "bold"),
                            bg='orange')
        self.status.pack(side='top')

        # self.next = Frame(self.frame, width=Game.SIDE, height=100, bg='gray')
        self.nextCanvas = Canvas(
            self.game_frame,
            width=Game.SIDE,
            height=Game.NEXT_HEIGHT,
            bg='yellow')
        self.nextCanvas.pack(fill='both', side='top')

        self.root.mainloop()

    def timer(self):

        if self.create_new_game == True:
            self.first_shape = self.second_shape
            self.second_shape = choice(self.SHAPES)
            self.nextCanvas.destroy()
            self.nextCanvas = Canvas(self.game_frame, width=Game.SIDE, height=Game.NEXT_HEIGHT, bg='yellow')
            self.nextCanvas.pack(fill='both', side='top')
            for point in self.second_shape[1:]:
                check_shape(self, self.second_shape[0], self.kuroojyo, self.mushi, self.syogun, self.murasaki, self.tonakai, self.ryu, self.akanin)
                self.nextCanvas.create_image(point[0] * Shape.BOX_SIZE + 40 + Shape.BOX_SIZE / 2,
                                          point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE / 2 + 40,
                                          image=self.image)
            self.current_shape = Shape(self.canvas, self.kuroojyo, self.mushi, self.syogun, self.murasaki, self.tonakai, self.ryu, self.akanin, self.first_shape)
            self.create_new_game = False

        if not self.current_shape.fall():
            self.first_shape = self.second_shape
            self.second_shape = choice(self.SHAPES)
            self.nextCanvas.destroy()
            self.nextCanvas = Canvas(self.game_frame, width=Game.SIDE, height=Game.NEXT_HEIGHT, bg='yellow')
            self.nextCanvas.pack(fill='both', side='top')
            for point in self.second_shape[1:]:
                check_shape(self, self.second_shape[0], self.kuroojyo, self.mushi, self.syogun, self.murasaki, self.tonakai, self.ryu, self.akanin)

                self.nextCanvas.create_image(point[0] * Shape.BOX_SIZE + 40 + Shape.BOX_SIZE / 2,
                                             point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE / 2 + 40,
                                             image=self.image)

            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level ** 2 * lines ** 2
                self.status_var.set("Level: %d, Score: %d" %
                                    (self.level, self.score))

            self.current_shape = Shape(self.canvas, self.kuroojyo, self.mushi, self.syogun, self.murasaki, self.tonakai, self.ryu, self.akanin, self.first_shape)
            if self.is_game_over():
                self.create_new_game = True
                self.game_over()

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                self.speed -= 5
                self.counter = 0
                self.status_var.set("Level: %d, Score: %d" %
                                    (self.level, self.score))

        self.root.after(self.speed, self.timer)

    def handle_events(self, event):
        if event.keysym == "Left": self.current_shape.move(-1, 0)
        if event.keysym == "Right": self.current_shape.move(1, 0)
        if event.keysym == "Down": self.current_shape.move(0, 1)
        if event.keysym == "Up": self.current_shape.rotate()

    def is_game_over(self):
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        shape_boxes_coords = [(self.canvas.coords(box)[1] + Shape.BOX_SIZE) for box
                              in self.current_shape.boxes]
        all_boxes = self.canvas.find_all()
        all_boxes_coords = {k: v for k, v in
                            zip(all_boxes, [(self.canvas.coords(box)[1] + Shape.BOX_SIZE)
                                            for box in all_boxes])}
        lines_to_check = set(shape_boxes_coords)
        boxes_to_check = dict((k, v) for k, v in all_boxes_coords.items()
                              if any(v == line for line in lines_to_check))
        counter = Counter()
        for box in boxes_to_check.values(): counter[box] += 1
        complete_lines = [k for k, v in counter.items()
                          if v == ((Game.WIDTH) / Shape.BOX_SIZE)]

        if not complete_lines: return False

        for k, v in boxes_to_check.items():
            if v in complete_lines:
                self.canvas.delete(k)
                del all_boxes_coords[k]

        for (box, coords) in all_boxes_coords.items():
            for line in complete_lines:
                if coords < line:
                    self.canvas.move(box, 0, Shape.BOX_SIZE)
        return len(complete_lines)

    def game_over(self):
        self.canvas.delete(tkinter.ALL)

        self.create_new_game = True
        messagebox.showinfo(
            "Game Over",
            "You scored %d points." % self.score)
        self.level = 1
        self.score = 0
        self.speed = 500
        self.counter = 0
        self.status_var.set("Level: %d, Score: %d" %
                            (self.level, self.score))


class Shape:
    BOX_SIZE = 40
    START_POINT = (Game.WIDTH) / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE

    def __init__(self, canvas, kuroojyo, mushi, syogun, murasaki, tonakai, ryu, akanin, shape):
        self.boxes = []  # the squares drawn by canvas.create_rectangle()
        # self.shape = choice(Shape.SHAPES)  # a random shape
        self.color = shape[0]
        self.canvas = canvas
        check_shape(self, shape[0], kuroojyo, mushi, syogun, murasaki, tonakai, ryu, akanin)

        for point in shape[1:]:
            box = canvas.create_image(point[0] * Shape.BOX_SIZE + Shape.START_POINT + Shape.BOX_SIZE/2,
                                      point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE/2,
                                      image=self.image)
            self.boxes.append(box)

    def move(self, x, y):
        if not self.can_move_shape(x, y):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        if not self.can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        '''Rotates the shape clockwise.'''
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def get_move_coords(box):
            '''Return (x, y) boxes needed to rotate a box around the pivot.'''
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / self.BOX_SIZE
            y_move = (x_diff - y_diff) / self.BOX_SIZE
            return x_move, y_move

        # Check if shape can legally move
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move):
                return False

        # Move shape
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box,
                             x_move * self.BOX_SIZE,
                             y_move * self.BOX_SIZE)

        return True

    def can_move_box(self, box, x, y):
        '''Check if box can move (x, y) boxes.'''
        x = x * Shape.BOX_SIZE
        y = y * Shape.BOX_SIZE
        coords = self.canvas.coords(box)
        # Returns False if moving the box would overrun the screen
        if coords[1] + Shape.BOX_SIZE/2 + y > Game.HEIGHT: return False
        if coords[0] - Shape.BOX_SIZE/2 + x < 0: return False
        if coords[0] + Shape.BOX_SIZE/2 + x > (Game.WIDTH): return False

        # Returns False if moving box (x, y) would overlap another box
        overlap = set(self.canvas.find_overlapping(
            (coords[0] + coords[0]) / 2 + x,
            (coords[1] + coords[1]) / 2 + y,
            (coords[0] + coords[0]) / 2 + x,
            (coords[1] + coords[1]) / 2 + y
        ))
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items: return False

        return True

    def can_move_shape(self, x, y):
        '''Check if the shape can move (x, y) boxes.'''
        for box in self.boxes:
            if not self.can_move_box(box, x, y): return False
        return True


if __name__ == "__main__":
    game = Game()
    game.start()