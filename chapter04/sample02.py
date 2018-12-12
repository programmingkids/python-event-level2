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


root.mainloop()
