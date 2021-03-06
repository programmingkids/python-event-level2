# ボックスのサイズ。これは固定値で20
BOX_SIZE = 20
# BOX_SIZEの倍数にします
WINDOW_WIDTH = 300
# 高さは自由に設定していいです
WINDOW_HEIGHT = 500

# ブロックの形
BLOCKS = (
    ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),  # 四角
    ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # 直線
    ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),  # 右L字
    ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),  # 左L字
    ("green", (0, 1), (1, 1), (1, 0), (2, 0)),  # 右カギ形
    ("red", (0, 0), (1, 0), (1, 1), (2, 1)),  # 左カギ形
    ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),  # 土形
)
