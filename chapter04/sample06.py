from tkinter import *

# 画面の横幅
WINDOW_WIDTH = 280
# 画面の高さ
WINDOW_HEIGHT = 500
# ブロックのサイズ
BOX_SIZE = 20

# Tkinter
root = Tk()
root.title("Puzzle")

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

canvas.create_rectangle(BOX_SIZE*6,BOX_SIZE*0,BOX_SIZE*7,BOX_SIZE*1, fill="green")
canvas.create_rectangle(BOX_SIZE*,BOX_SIZE*,BOX_SIZE*,BOX_SIZE*, fill="green")
canvas.create_rectangle(BOX_SIZE*,BOX_SIZE*,BOX_SIZE*,BOX_SIZE*, fill="green")
canvas.create_rectangle(BOX_SIZE*,BOX_SIZE*,BOX_SIZE*,BOX_SIZE*, fill="green")

root.mainloop()

