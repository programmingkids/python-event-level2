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

canvas.create_rectangle(0,0,BOX_SIZE,BOX_SIZE, fill="red")
canvas.create_rectangle(BOX_SIZE,0,BOX_SIZE*2,BOX_SIZE, fill="blue")
canvas.create_rectangle(BOX_SIZE,BOX_SIZE,BOX_SIZE*2,BOX_SIZE*2, fill="green")

root.mainloop()
