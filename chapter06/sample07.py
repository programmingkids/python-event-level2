from tkinter import *

# 画面の横幅
WINDOW_WIDTH = 280
# 画面の高さ
WINDOW_HEIGHT = 500
# ブロックのサイズ
BOX_SIZE = 20
# 落下速度
SPEED = 200


def move():
    # blockはリストです。リスト内のボックスを1個ずつ取り出し、Y方向に移動させます
    for box in block:
        # 第1引数は移動対象ボックス、
        # 第2引数はX方向の移動量、今回は実質0
        # 第3引数はY方向の移動量、今回はBOX_SIZEだけ移動
        canvas.move(box, 0 * BOX_SIZE, 1 * BOX_SIZE)
    root.after(SPEED, move)


# Tkinter
root = Tk()
root.title("Puzzle")

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()




# 200ミリ秒おきに「move」を実行します
root.after(SPEED, move)
# メインの画面を表示します
root.mainloop()
