import math
import tkinter
from tkinter import Canvas, Label, Tk, StringVar
from tkinter import messagebox
from random import choice
from collections import Counter

# これは固定にしておく
BOX_SIZE = 20
# BOX_SIZEの倍数にします
WINDOW_WIDTH = 280
# 高さは自由に設定していいです
WINDOW_HEIGHT = 500

# ブロックの形
BLOCKS = (
    ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),  # 四角
    ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # 直線
    ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),  # 右L字
    ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),  # 左L字
    ("green", (0, 1), (1, 1), (1, 0), (2, 0)),  # 右カギ形
    ("red", (0, 0), (1, 0), (1, 1), (2, 1)),  # 左カギ形
    ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),  # 土形
)


class Game:
    def __init__(self):
        # レベル
        self.level = 1
        # 点数
        self.score = 0
        # 表示速度
        self.speed = 500
        # レベルアップのためのカウンタ用変数
        self.counter = 0
        self.create_new_game = True

        # メインのフレーム
        self.root = Tk()
        self.root.title("Puzzle")
        label_font = ("System", 10)
        # レベルとスコアを表示する文字
        self.status_var = StringVar()
        self.status_var.set("レベル： 1  スコア： 0")
        # レベルとスコアを表示するラベル
        self.status_label = Label(self.root, textvariable=self.status_var, font=label_font)
        self.status_label.pack()
        # ブロックを表示するキャンバス
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()
        # キー操作に対応するイベントを登録します
        self.root.bind("<Key>", self.event_handler)

    def event_handler(self, event):
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
        # フレーム表示
        self.root.mainloop()

    def timer(self):
        if self.create_new_game == True:
            # ゲームを開始時点で新しいブロックを作ります
            self.current_block = Block(self.canvas)
            self.create_new_game = False

        if not self.current_block.fall():
            # 画面の下端に到達、または他のブロックに重なったので移動が終了しました
            # そろっているブロックは削除します
            lines = self.remove_complete_lines()
            # 削除しなかった場合、False、削除した場合、削除行数が返ります
            if lines:
                # 削除した行数に応じて、スコアアップ
                # 10 * levelの2乗 * linesの2乗
                self.score += 10 * self.level ** 2 * lines ** 2
                # スコアを表示
                self.status_var.set("レベル： %d  スコア： %d" % (self.level, self.score))

            # 新しいブロックを作成して、画面に表示します
            self.current_block = Block(self.canvas)

            # ゲームオーバーの判定
            if self.is_game_over():
                # ゲームオーバーなので終了処理
                self.create_new_game = True
                self.game_over()

            # ブロックを5個処理するとレベルアップする機能
            self.counter += 1
            if self.counter == 5:
                # レベルアップ
                self.level += 1
                # スピードアップ
                self.speed -= 20
                # レベルアップカウンタを初期化
                self.counter = 0
                # スコアを表示
                self.status_var.set("レベル： %d  スコア： %d" % (self.level, self.score))

        # self.speedの間隔でself.timerを何度も呼び出す
        self.root.after(self.speed, self.timer)

    # ゲームオーバーの判定
    def is_game_over(self):
        # ブロックが移動することができない場合、ゲームオーバー
        for box in self.current_block.boxes:
            if not self.current_block.can_move_box(box, 0, 1):
                # 移動できないのでゲームオーバー
                return True
        # ゲームは継続
        return False

    # 落下が終了した後に、ボックスがそろっている行があれば、削除します
    def remove_complete_lines(self):
        # 現在の処理対象ボックスの右下角のY座標をリストに代入します
        block_boxes_coords = []
        for box in self.current_block.boxes:
            # coords は[x1, y1, x2, y2]の形式で座標を取得します
            # x1, y1はボックスの左上角、x2とy2は右下角
            block_boxes_coords.append(self.canvas.coords(box)[3])

        # キャンバス内のすべてのオブジェクトを取り出します
        all_boxes = self.canvas.find_all()

        # 全ボックスの右下角のY座標をリストに追加します
        all_boxes_y = []
        for box in all_boxes:
            all_boxes_y.append(self.canvas.coords(box)[3])
        # 全ボックスと座標を合体したリストにします
        zipped = zip(all_boxes, all_boxes_y)

        # 全てのオブジェクトを辞書にします
        # 辞書のキーはオブジェクトID、辞書の値はY座標
        all_boxes_coords = {}
        for d in zipped:
            all_boxes_coords[d[0]] = d[1]

        # setに変換して、重複値を除く
        lines_to_check = set(block_boxes_coords)

        # 現在処理中のブロックのボックスと同じ行のボックスを取り出す
        boxes_to_check = {}
        for k, v in all_boxes_coords.items():
            # 現在のボックスと同じ行のボックスを取り出します
            for line in lines_to_check:
                if v == line:
                    # Y座標が同じであれば同じ行とします
                    boxes_to_check[k] = v
                    break

        # 同じ行にあるボックス数を計算します
        counter = Counter()
        for box in boxes_to_check.values():
            counter[box] += 1

        # 同じ行のボックス数が、「ウィンドウの幅/BOX_SIZE」と同じなら
        # 行がボックスで埋まったことになります
        complete_lines = []
        for k, v in counter.items():
            if v == (WINDOW_WIDTH / BOX_SIZE):
                # 1行がそろったので削除対象の行を追加します
                complete_lines.append(k)

        # 削除する行がない場合、ここで処理は終わり、Falseを返します
        if not complete_lines: return False

        # そろっている行のブロックを削除します
        for k, v in boxes_to_check.items():
            # 対象のブロックが、削除する行に含まれている
            if v in complete_lines:
                # 対象のブロックをキャンバスから消します
                self.canvas.delete(k)
                # 全てのブロックを保持するリストからも消します
                del all_boxes_coords[k]

        # 削除した行の分だけ、全体を下に移動させる
        for (box, coords) in all_boxes_coords.items():
            for line in complete_lines:
                # 削除行した行よりも上に位置するかどうかを判定します
                if coords < line:
                    # 削除した行よりも上なので、ボックスを下方向に移動
                    self.canvas.move(box, 0, BOX_SIZE)
        return len(complete_lines)

    # ゲーム―オーバー処理
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
        self.start_point_x = (math.floor(WINDOW_WIDTH / BOX_SIZE / 2 ) - 1) * BOX_SIZE

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

    # ブロックを時計回りに回転します。今回は逆回転はしない
    def rotate(self):
        boxes = self.boxes[:]
        # 回転の軸になるボックスを指定します。ピボットと呼びます
        pivot = boxes.pop(2)

        def get_move_coords(box):
            # ピボットのボックスを軸として、回転するべき座標を計算します
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / BOX_SIZE
            y_move = (x_diff - y_diff) / BOX_SIZE
            return x_move, y_move

        # ボックスが移動可能かを判定します
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move):
                # 移動不可なので、回転しません
                return False

        # それぞれのボックスを移動させて、回転します
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
        # x1, y1はボックスの左上角、x2とy2は右下角
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
