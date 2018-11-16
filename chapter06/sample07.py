import tkinter

# tkinterを初期化する
root = tkinter.Tk()

# タイトルを設定する
root.title("サンプル10")
# ウィンドウのサイズの設定
root.geometry("896x640")
# ウィンドウの最小サイズの設定（このサイズより小さくなりません）
root.minsize(896, 640)
# ウィンドウの最大サイズの設定（このサイズより大きくなりません）
root.maxsize(896, 640)

# キャンバスを作成 背景色は「白」、幅と高さはウィンドウと同じサイズにする
canvas = tkinter.Canvas(bg="white",width=896, height=640)
# キャンバスをウィンドウに配置
canvas.place(x=0, y=0)

# 画像ファイルを読み込み、リストに代入します
images = [
    tkinter.PhotoImage(file="../images/robot.png"),
    tkinter.PhotoImage(file="../images/robot2.png"),
    tkinter.PhotoImage(file="../images/robot3.png"),
    tkinter.PhotoImage(file="../images/robot4.png"),
    tkinter.PhotoImage(file="../images/robot5.png"),
    tkinter.PhotoImage(file="../images/robot6.png"),
    tkinter.PhotoImage(file="../images/robot7.png"),
]

# リスト内の画像をキャンバスに表示します
for i in range(len(images)):
    canvas.create_image(32 + i * 64, 32, image=images[i])

# 画面を表示します
root.mainloop()
