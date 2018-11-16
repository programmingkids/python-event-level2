from tkinter import *

# 画面の横幅
WINDOW_WIDTH = 280
# 画面の高さ
WINDOW_HEIGHT = 500
# ブロックのサイズ
BOX_SIZE = 20
# 落下速度
SPEED = 200


def create_block():
    box_a = canvas.create_rectangle(BOX_SIZE * 6, BOX_SIZE * 0, BOX_SIZE * 7, BOX_SIZE * 1, fill="red")
    box_b = canvas.create_rectangle(BOX_SIZE * 7, BOX_SIZE * 0, BOX_SIZE * 8, BOX_SIZE * 1, fill="red")
    box_c = canvas.create_rectangle(BOX_SIZE * 6, BOX_SIZE * 1, BOX_SIZE * 7, BOX_SIZE * 2, fill="red")
    box_d = canvas.create_rectangle(BOX_SIZE * 7, BOX_SIZE * 1, BOX_SIZE * 8, BOX_SIZE * 2, fill="red")

    # ボックスをまとめたリストを作ります
    block = [box_a, box_b, box_c, box_d]
    return block


def fall():
    global current_block
    if( can_move_block(current_block, 0, 1) == True):
        # 移動することができるのでY方向に移動
        move(0, 1)
    else:
        # 異動することができないので、新しいブロックを作ります
        current_block = create_block()
    root.after(SPEED, fall)


def move(x, y):
    global current_block
    if( can_move_block(current_block, x, y) == True):
        # blockはリストです。リスト内のボックスを1個ずつ取り出し、Y方向に移動させます
        for box in current_block:
            # 第1引数は移動対象ボックス、
            # 第2引数はX方向の移動量、今回は実質0
            # 第3引数はY方向の移動量、今回はBOX_SIZEだけ移動
            canvas.move(box, x * BOX_SIZE, y * BOX_SIZE)


def can_move_box(box, x, y):
    # xとyは移動させる数なので、BOX_SIZEをかけて、移動量にする
    x = x * BOX_SIZE
    y = y * BOX_SIZE

    # boxの現在の座標を取得する
    # coords は[x1, y1, x2, y2]の形式で座標を取得します
    # x1, y1はボックスの左上角、x2とy2は右下角
    coords = canvas.coords(box)

    # boxの右下のY座標にyを加算した値が、ウィンドウの高さより大きい場合、移動不可
    if coords[3] + y > WINDOW_HEIGHT:
        return False
    # boxの左上のX座標にxを加算した値が、0より小さい場合、移動不可
    if coords[0] + x < 0:
        return False
    # boxの右下のX座標にxを加算した値が、ウィンドウの幅よりも大きい場合、移動不可
    if coords[2] + x > WINDOW_WIDTH:
        return False

    # 移動先の座標を計算する
    new_x1 = (coords[0] + coords[2]) / 2 + x
    new_y1 = (coords[1] + coords[3]) / 2 + y
    new_x2 = (coords[0] + coords[2]) / 2 + x
    new_y2 = (coords[1] + coords[3]) / 2 + y
    # 移動先の座標と重なっているボックスがあればsetで返す
    # 重なっているボックスのオブジェクトIDが返ります
    overlap = set(canvas.find_overlapping(new_x1, new_y1, new_x2, new_y2))

    # Canvas内の全てのオブジェクトから、現在のボックス以外をsetで取り出す
    other_items = set(canvas.find_all()) - set(current_block)
    # 移動先で重複しているオブジェクトが現在のボックスではない場合、Trueとなります
    if overlap & other_items:
        return False
    # 移動OK
    return True


def can_move_block(block, x, y):
    for box in block:
        # ボックスの移動数は「x, y」です
        # 「x, y」の移動が可能なのかを判定します
        if not can_move_box(box, x, y):
            return False
    return True


def event_handler(event):
    if event.keysym == "Left":
        move(-1, 0)
    if event.keysym == "Right":
        move(1, 0)
    if event.keysym == "Down":
        move(0, 1)


# Tkinter
root = Tk()
root.title("Puzzle")

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# キーをクリックされたときに移動します
root.bind("<Key>", event_handler)
# 最初に新しいブロックを作ります
current_block = create_block()
# 200ミリ秒おきに「move」を実行します
root.after(SPEED, fall)
# メインの画面を表示します
root.mainloop()
