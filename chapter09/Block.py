from random import choice
from chapter09.Setting import *


# ブロックの形を表すクラス
class Block:

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
        # xとyは移動させる座標なので、BOX_SIZEをかけて、移動量にする
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
