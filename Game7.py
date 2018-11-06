import tkinter as tk
from tkinter import Label, StringVar, Frame

def raise_frame(frame):
    frame.tkraise()

root = tk.Tk()
#メインウィンドウのタイトルを変更
root.title("Tkinter test")
#メインウィンドウを640x480にする
root.geometry("640x480")
frame1 = Frame(root, width=640, height=480)

frame1.grid(row=0, column=0, sticky='news')
frame2 = Frame(root, width=200, height=200)
frame2.grid(row=0, column=0, sticky='news' )
status_var = StringVar()
status_var.set("パズルゲーム")
label1 = Label(frame1, textvariable=status_var,font=("Helvetica", 30, "bold"),bg='orange')
label1.place(x=200, y=130)
# ボタン
btn1 = tk.Button(frame1, text='開始',bg='orange', command=lambda:raise_frame(frame2))

btn1.place(x=300, y=300)

status_var2 = StringVar()
status_var2.set("パズルゲーム2")
label = Label(frame2, textvariable=status_var2,font=("Helvetica", 20, "bold"),bg='orange').pack()
#表示
# label.place(x=240, y=140)

# ボタン
btn = tk.Button(frame2, text='開始',bg='orange', command=lambda:raise_frame(frame1)).pack()
# btn.place(x=300, y=300)

raise_frame(frame1)
root.mainloop()