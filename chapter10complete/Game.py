from tkinter import Canvas, Label, Tk, StringVar, ALL
from tkinter import messagebox
from collections import Counter
from chapter10complete.Block import Block
from chapter10complete.Setting import *


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
        if event.keysym == "space":
            self.current_block.rotate_reverse()

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
        self.all_boxes_coords = {}
        for d in zipped:
            self.all_boxes_coords[d[0]] = d[1]

        # setに変換して、重複値を除く
        lines_to_check = set(block_boxes_coords)

        # 現在処理中のブロックのボックスと同じ行のボックスを取り出す
        boxes_to_check = {}
        for k, v in self.all_boxes_coords.items():
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
        self.complete_lines = []
        for k, v in counter.items():
            if v == (WINDOW_WIDTH / BOX_SIZE):
                # 1行がそろったので削除対象の行を追加します
                self.complete_lines.append(k)

        # 削除する行がない場合、ここで処理は終わり、Falseを返します
        if not self.complete_lines: return False

        # そろっている行のブロックを削除します
        remove_boxes = []
        for k, v in boxes_to_check.items():
            # 対象のブロックが、削除する行に含まれている
            if v in self.complete_lines:
                # 対象のブロックをキャンバスから消します
                #self.canvas.delete(k)
                # 全てのブロックを保持するリストからも消します
                del self.all_boxes_coords[k]
                remove_boxes.append(k)
        # スライドして削除する
        self.slide_away(remove_boxes)
        return len(self.complete_lines)

    # ゲーム―オーバー処理
    def game_over(self):
        # 全てのオブジェクトを削除
        self.canvas.delete(ALL)
        # メッセージ表示
        messagebox.showinfo("ゲームオーバー","スコア：%d " % self.score)
        # 画面を閉じる
        self.root.quit()

    def slide_away(self, remove_boxes):
        for remove_box in remove_boxes:
            # BOX_SIZE分だけ左に移動
            self.canvas.move(remove_box,BOX_SIZE * -1, 0)
            coords = self.canvas.coords(remove_box)
            if coords[2] < 0:
                # 画面から消えたら、削除
                self.canvas.delete(remove_box)
                remove_boxes.remove(remove_box)

        if remove_boxes:
            # 削除対象リストにまだボックスが存在する場合、再度呼び出す
            self.root.after(10, self.slide_away, remove_boxes)
        else:
            # すべて削除できたので、削除したボックスより上部を下に移動
            for (box, coords) in self.all_boxes_coords.items():
                for line in self.complete_lines:
                    # 削除行した行よりも上に位置するかどうかを判定します
                    if coords < line:
                        # 削除した行よりも上なので、ボックスを下方向に移動
                        self.canvas.move(box, 0, BOX_SIZE)
