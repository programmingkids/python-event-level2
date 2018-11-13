import tkinter
from tkinter import Canvas, Label, Tk, StringVar
from tkinter import messagebox
from random import choice
from collections import Counter


WINDOW_WIDTH = 300
WINDOW_HEIGHT = 500
BOX_SIZE = 20


class Game():

    def __init__(self):
        self.level = 1
        self.score = 0
        self.speed = 500
        self.counter = 0
        self.create_new_game = True

        self.root = Tk()
        self.root.title("Puzzle")

        label_font = ("System", 10)

        self.status_var = StringVar()
        self.status_var.set("レベル： 1  スコア： 0")
        self.status_label = Label(self.root, textvariable=self.status_var, font=label_font)
        self.status_label.pack()

        self.canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)

    def handle_events(self, event):
        if event.keysym == "Left":
            self.current_shape.move(-1, 0)
        if event.keysym == "Right":
            self.current_shape.move(1, 0)
        if event.keysym == "Down":
            self.current_shape.move(0, 1)
        if event.keysym == "Up":
            self.current_shape.rotate()

    def start(self):
        self.timer()
        self.root.mainloop()

    def timer(self):
        '''Every self.speed ms, attempt to cause the current_shape to fall().
        If fall() returns False, create a new shape and check if it can fall.
        If it can't, then the game is over.

        '''
        if self.create_new_game == True:
            self.current_shape = Shape(self.canvas)
            self.create_new_game = False

        if not self.current_shape.fall():
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level ** 2 * lines ** 2
                self.status_var.set("Level: %d, Score: %d" %
                                    (self.level, self.score))

            self.current_shape = Shape(self.canvas)
            if self.is_game_over():
                # TODO This is a problem. You rely on the timer method to
                # create a new game rather than creating it here. As a
                # result, there is an intermittent error where the user
                # event keypress Down eventually causes can_move_box
                # to throw an IndexError, since the current shape has
                # no boxes. Instead, you need to cleanly start a new
                # game. I think refactoring start() might help a lot
                # here.
                #
                # Furthermore, starting a new game currently doesn't reset
                # the levels. You should place all your starting constants
                # in the same place so it's clear what needs to be reset
                # when.
                self.create_new_game = True
                self.game_over()

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                self.speed -= 20
                self.counter = 0
                self.status_var.set("Level: %d, Score: %d" %
                                    (self.level, self.score))

        self.root.after(self.speed, self.timer)


    def is_game_over(self):
        '''Check if a newly created shape is able to fall.
        If it can't fall, then the game is over.
        '''
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        shape_boxes_coords = [self.canvas.coords(box)[3] for box
                              in self.current_shape.boxes]
        all_boxes = self.canvas.find_all()
        all_boxes_coords = {k: v for k, v in
                            zip(all_boxes, [self.canvas.coords(box)[3]
                                            for box in all_boxes])}
        lines_to_check = set(shape_boxes_coords)
        boxes_to_check = dict((k, v) for k, v in all_boxes_coords.items()
                              if any(v == line for line in lines_to_check))
        counter = Counter()
        for box in boxes_to_check.values(): counter[box] += 1
        complete_lines = [k for k, v in counter.items()
                          if v == (WINDOW_WIDTH / BOX_SIZE) - 1]

        if not complete_lines: return False

        for k, v in boxes_to_check.items():
            if v in complete_lines:
                self.canvas.delete(k)
                del all_boxes_coords[k]

        # TODO Would be cooler if the line flashed or something
        for (box, coords) in all_boxes_coords.items():
            for line in complete_lines:
                if coords < line:
                    self.canvas.move(box, 0, BOX_SIZE)
        return len(complete_lines)

    def game_over(self):
        self.canvas.delete(tkinter.ALL)
        messagebox.showinfo(
            "Game Over",
            "You scored %d points." % self.score)


# ブロックの形を表すクラス
class Shape:
    #START_POINT = WINDOW_WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    # Shapeが最初に登場する時のX座標
    START_POINT = WINDOW_WIDTH / 2 - BOX_SIZE

    # ブロックの形
    SHAPES = (
        ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),  # square
        ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
        ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),  # right el
        ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),  # left el
        ("green", (0, 1), (1, 1), (1, 0), (2, 0)),  # right wedge
        ("red", (0, 0), (1, 0), (1, 1), (2, 1)),  # left wedge
        ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),  # symmetrical wedge
    )

    def __init__(self, canvas):
        self.boxes = []  # the squares drawn by canvas.create_rectangle()
        self.shape = choice(Shape.SHAPES)  # a random shape
        self.color = self.shape[0]
        self.canvas = canvas

        for point in self.shape[1:]:
            box = canvas.create_rectangle(
                point[0] * BOX_SIZE + Shape.START_POINT,
                point[1] * BOX_SIZE,
                point[0] * BOX_SIZE + BOX_SIZE + Shape.START_POINT,
                point[1] * BOX_SIZE + BOX_SIZE,
                fill=self.color)
            self.boxes.append(box)

    def move(self, x, y):
        '''Moves this shape (x, y) boxes.'''
        if not self.can_move_shape(x, y):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, x * BOX_SIZE, y * BOX_SIZE)
            return True

    def fall(self):
        '''Moves this shape one box-length down.'''
        if not self.can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * BOX_SIZE, 1 * BOX_SIZE)
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
            x_move = (- x_diff - y_diff) / BOX_SIZE
            y_move = (x_diff - y_diff) / BOX_SIZE
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
                             x_move * BOX_SIZE,
                             y_move * BOX_SIZE)

        return True

    def can_move_box(self, box, x, y):
        '''Check if box can move (x, y) boxes.'''
        x = x * BOX_SIZE
        y = y * BOX_SIZE
        coords = self.canvas.coords(box)

        # Returns False if moving the box would overrun the screen
        if coords[3] + y > WINDOW_HEIGHT: return False
        if coords[0] + x < 0: return False
        if coords[2] + x > WINDOW_WIDTH: return False

        # Returns False if moving box (x, y) would overlap another box
        overlap = set(self.canvas.find_overlapping(
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y,
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y
        ))
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items: return False

        return True

    def can_move_shape(self, x, y):
        '''Check if the shape can move (x, y) boxes.'''
        for box in self.boxes:
            if not self.can_move_box(box, x, y): return False
        return True


game = Game()
game.start()
