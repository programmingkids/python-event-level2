import tkinter
from tkinter import Canvas, Label, Tk, StringVar
from tkinter import messagebox
from random import choice
from collections import Counter


WINDOW_WIDTH = 300
WINDOW_HEIGHT = 500
BOX_SIZE = 20

# ブロックの形
BLOCKS = (
    ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),  # square
    ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
    ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),  # right el
    ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),  # left el
    ("green", (0, 1), (1, 1), (1, 0), (2, 0)),  # right wedge
    ("red", (0, 0), (1, 0), (1, 1), (2, 1)),  # left wedge
    ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),  # symmetrical wedge
)


class Game():
    def __init__(self):
        # レベル
        self.level = 1
        # 点数
        self.score = 0
        # 表示速度
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
            self.current_block.move(-1, 0)
        if event.keysym == "Right":
            self.current_block.move(1, 0)
        if event.keysym == "Down":
            self.current_block.move(0, 1)
        if event.keysym == "Up":
            self.current_block.rotate()

    def start(self):
        # タイマー処理を開始します
        self.timer()
        self.root.mainloop()

    def timer(self):
        if self.create_new_game == True:
            # 新しいブロックを作ります
            self.current_block = Block(self.canvas)
            self.create_new_game = False

        if not self.current_block.fall():
            # 画面の下端に到達、または他のブロックに重なったので移動が終了しました
            # そろっているブロックは削除します
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level ** 2 * lines ** 2
                self.status_var.set("Level: %d, Score: %d" %
                                    (self.level, self.score))

            self.current_block = Block(self.canvas)
            if self.is_game_over():
                # ゲームオーバーなので終了処理
                self.create_new_game = True
                self.game_over()

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                self.speed -= 20
                self.counter = 0
                self.status_var.set("Level: %d, Score: %d" %
                                    (self.level, self.score))

        # selp.speedの間隔でself.timerを何度も呼び出す
        self.root.after(self.speed, self.timer)


    def is_game_over(self):
        '''Check if a newly created shape is able to fall.
        If it can't fall, then the game is over.
        '''
        for box in self.current_block.boxes:
            if not self.current_block.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        block_boxes_coords = [self.canvas.coords(box)[3] for box
                              in self.current_block.boxes]
        all_boxes = self.canvas.find_all()
        all_boxes_coords = {k: v for k, v in
                            zip(all_boxes, [self.canvas.coords(box)[3]
                                            for box in all_boxes])}
        lines_to_check = set(block_boxes_coords)
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
        # 全てのオブジェクトを削除
        self.canvas.delete(tkinter.ALL)
        # メッセージ表示
        messagebox.showinfo("ゲームオーバー","スコア：%d " % self.score)
        # 画面を閉じる
        self.root.quit()


# ブロックの形を表すクラス
class Block:
    # コンストラクタでブロックを作成
    def __init__(self, canvas):
        self.start_point_x = WINDOW_WIDTH / 2 - BOX_SIZE

        # キャンバスに描かれるボックスをリストで保存します
        self.boxes = []
        # Shape.SHAPESの中からランダムに取り出す
        self.block = choice(BLOCKS)
        self.color = self.block[0]
        self.canvas = canvas

        for point in self.block[1:]:
            # ボックスを最初の位置に表示します
            box = canvas.create_rectangle(
                point[0] * BOX_SIZE + self.start_point_x,
                point[1] * BOX_SIZE,
                point[0] * BOX_SIZE + BOX_SIZE + self.start_point_x,
                point[1] * BOX_SIZE + BOX_SIZE,
                fill=self.color)
            # 表示したボックスをリストに格納します
            self.boxes.append(box)

    # ブロックを動かす処理
    def move(self, x, y):
        # ブロックを動かすことができるのか判定する
        if not self.can_move_block(x, y):
            # 移動不可
            return False
        else:
            # 移動可能なので、実際に移動して表示させる
            for box in self.boxes:
                # 第1引数は移動対象ボックス、
                # 第2引数はX方向の移動量、今回は実質0
                # 第3引数はY方向の移動量、今回はBOX_SIZEだけ移動
                self.canvas.move(box, x * BOX_SIZE, y * BOX_SIZE)
            # 移動成功なので、Trueを返します
            return True

    # ブロックを下に動かす処理
    def fall(self):
        # ブロックを動かすことができるのか判定する
        if not self.can_move_block(0, 1):
            # 下に移動不可
            return False
        else:
            # 下に移動可能なので、実際に移動して表示させる
            # 全てのボックスをY方向に移動させる
            for box in self.boxes:
                # 第1引数は移動対象ボックス、
                # 第2引数はX方向の移動量、今回は実質0
                # 第3引数はY方向の移動量、今回はBOX_SIZEだけ移動
                self.canvas.move(box, 0 * BOX_SIZE, 1 * BOX_SIZE)
            # 移動成功なので、Trueを返します
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
            self.canvas.move(box, x_move * BOX_SIZE, y_move * BOX_SIZE)
        return True

    # 現在のブロック内のボックスを動かすことができるかを判定します
    def can_move_box(self, box, x, y):
        # xとyは移動させる数なので、BOX_SIZEをかけて、移動量にする
        x = x * BOX_SIZE
        y = y * BOX_SIZE

        # boxの現在の座標を取得する
        # coords は[x1, y1, x2, y2]の形式で座標を取得します
        coords = self.canvas.coords(box)

        # boxの右下のY座標にyを加算した値が、ウィンドウの高さより大きい場合、移動不可
        if coords[3] + y > WINDOW_HEIGHT: return False
        # boxの左上のX座標にxを加算した値が、0より小さい場合、移動不可
        if coords[0] + x < 0: return False
        # boxの右下のX座標にxを加算した値が、ウィンドウの幅よりも大きい場合、移動不可
        if coords[2] + x > WINDOW_WIDTH: return False

        # 移動先の座標を計算する
        new_x1 = (coords[0] + coords[2]) / 2 + x
        new_y1 = (coords[1] + coords[3]) / 2 + y
        new_x2 = (coords[0] + coords[2]) / 2 + x
        new_y2 = (coords[1] + coords[3]) / 2 + y
        # 移動先の座標と重なっているボックスがあればsetで返す
        # 重なっているボックスのオブジェクトIDが返ります
        overlap = set(self.canvas.find_overlapping(new_x1, new_y1, new_x2, new_y2))

        # Canvas内の全てのオブジェクトから、現在のボックス以外をsetで取り出す
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        # 移動先で重複しているオブジェクトが現在のボックスではない場合、Trueとなります
        if overlap & other_items:
            return False
        # 画面から飛び出さない、かつ他の要素にも重ならいない
        # 移動可能なのでTrueを返す
        return True

    # ブロックを動かすことができるのか判定する
    def can_move_block(self, x, y):
        # ブロックは複数のボックスからできています
        # 現在のブロックの全てのボックスをチェックします
        for box in self.boxes:
            # ボックスの移動数は「x, y」です
            # 「x, y」の移動が可能なのかを判定します
            if not self.can_move_box(box, x, y): return False
        # 全てのボックスが移動可能であればTrueを返します
        return True


game = Game()
game.start()
