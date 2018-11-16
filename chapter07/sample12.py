import tkinter


def draw_map():
    # マップ画像をキャンバスに表示します
    for x in range(14):
        for y in range(10):
            canvas.create_image(32 + x * 64, 32 + y * 64, image=map)
    # プレイヤ画像を表示します
    canvas.create_image(32 + player_x * 64, 32 + player_y * 64, image=player, tag="player")


def draw_player():
    canvas.coords("player", 32 + player_x * 64, 32 + player_y * 64)


def click_up_event(event):
    global player_x, player_y
    player_y -= 1
    if player_y < 0:
        player_y = 0
    draw_player()


def click_down_event(event):
    global player_x, player_y
    player_y += 1
    if player_y > 9:
        player_y = 9
    draw_player()


def click_left_event(event):
    global player_x, player_y
    player_x -= 1
    if player_x < 0:
        player_x = 0
    draw_player()


def click_right_event(event):
    global player_x, player_y
    player_x += 1
    if player_x > 13:
        player_x = 13
    draw_player()


# tkinterを初期化する
root = tkinter.Tk()

# タイトルを設定する
root.title("サンプル12")
# ウィンドウのサイズの設定
root.geometry("896x640")
# ウィンドウの最小サイズの設定（このサイズより小さくなりません）
root.minsize(896, 640)
# ウィンドウの最大サイズの設定（このサイズより大きくなりません）
root.maxsize(896, 640)

# マップ画像を読み込みます
map = tkinter.PhotoImage(file="../images/map01.png")
# プレイヤ画像を読み込みます
player = tkinter.PhotoImage(file="../images/chara01.png")

# プレイヤの座標設定
player_x = 6
player_y = 4

# キーボードイベントを登録する
frame = tkinter.Frame(root, width=896, height=640)
frame.bind("<Up>", click_up_event)
frame.bind("<Down>", click_down_event)
frame.bind("<Left>", click_left_event)
frame.bind("<Right>", click_right_event)
frame.focus_set()
frame.pack()

# キャンバスを作成 背景色は「青」、幅と高さはウィンドウと同じサイズにする
canvas = tkinter.Canvas(bg="white",width=896, height=640)
# キャンバスをウィンドウに配置
canvas.place(x=0, y=0)

# マップの初期表示
draw_map()

# 画面を表示します
root.mainloop()
