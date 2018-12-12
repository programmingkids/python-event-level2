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


# Tkinter
root = Tk()
root.title("Puzzle")

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# キーをクリックされたときに移動します
root.bind("<Key>", event_handler)
# 最初に新しいブロックを作ります
current_block = create_block()
# 200ミリ秒おきに「fall」を実行します
root.after(SPEED, fall)
# メインの画面を表示します
root.mainloop()
